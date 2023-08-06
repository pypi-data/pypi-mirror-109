
"""## Log Classifier

A binary classifier that takes as input a sentence and classifies if it is a log.

1. Parser - parses the text sentence to create a feature vector.
2. List of features:

    2.1 Contains date/time <br>
    2.2 Number of log levels: INFO | WARN | ERROR | DEBUG <br>
    2.3 Number of information on thread pool - eg [pool-3-thread-9] <br>
    2.4 Number Module/Component Name <br>
    2.5 Number of opening and closing brackets `[]` `{}`<br>
    2.6 Number of all CAPS words/tokens <br>
    2.7 Number of Camel Cased / Snake Cased words/tokens <br>
    2.8 Length of longest tokens <br>
"""

import re
import numpy as np
import pandas as pd
import pickle
import logging
import boto3
from dateutil.parser import parse
from string import punctuation
from typing import List



log = logging.getLogger(__name__)
logging.basicConfig()
log.setLevel(logging.INFO)

pd.set_option('display.max_colwidth', 1000)

"""
LogParser parses a sentence and creates a feature vector
"""
class LogParser:
    def __init__(self):
        self.dimentions = 9
        self.column_names = ['contains_data_time', 'number_log_level', 'number_pool_thread_references',
                            'number_component_refereences', 'number_balanced_parenthesis',
                            'number_all_caps_tokens', 'number_camel_cased_tokens', 'number_snake_cased_tokens',
                            'max_length_token']
        # tokens containing # of `.` >= this value will be considered code component reference.
        self.threshold_component_name = 2
        # Details of s3 where our model is saved for classification
        
        self.model_s3_bucket = 'concept-graph-dev'
        self.model_s3_key = 'log_classifier/our_model/log_classifier.pickle'
    
    def parse(self, input_text: str):
        log.debug(f"Parsing `{input_text}`")
        input_text = input_text.strip()
        input_text.replace('\n', '')
        input_tokens = input_text.split(" ")
        log.debug(f"Input tokens are {input_tokens}")
        feature_vector = np.zeros(shape=(self.dimentions))

        feature_vector[0] = any([ self.is_date_time(_token, True) for _token in input_tokens])
        feature_vector[1] = self.number_log_levels(input_text)
        feature_vector[2] = self.number_pool_thread_references(input_text)
        feature_vector[3] = sum([self.is_component(_token) for _token in input_tokens])
        feature_vector[4] = self.number_balanced_parenthesis(input_text, brace_type='square') \
                            + self.number_balanced_parenthesis(input_text, brace_type='curly') \
                            + self.number_balanced_parenthesis(input_text, brace_type='circle')
        feature_vector[5] = sum([self.is_all_caps(_token) for _token in input_tokens])
        feature_vector[6] = sum([self.number_camel_cased_tokens(_token) for _token in input_tokens])
        feature_vector[7] = sum([self.number_snake_cased_tokens(_token) for _token in input_tokens])
        feature_vector[8] = max([len(_token) for _token in input_tokens])
        
        return feature_vector
        
    def is_date_time(self, string, fuzzy=False):
        """
        fuzzy=True ignores unknown tokens in string
        """
        try: 
            parse(string, fuzzy=fuzzy)
            return True

        except Exception:
            return False
    
    def number_log_levels(self, input_text: str):
        log_level_regexp = r'INFO|WARN|WARNING|ERR|ERROR|DEBUG|FATAL|CRITICAL'
        return len(re.findall(log_level_regexp, input_text, re.IGNORECASE))
    
    def number_pool_thread_references(self, input_text: str):
        _input_text = input_text.lower()
        pool_regexp = r'pool'
        thread_regexp = r'thread'
        return len(re.findall(pool_regexp, _input_text)) + len(re.findall(thread_regexp, _input_text))
    
    def is_component(self, token: str):
        return token.lower().count('.') >= self.threshold_component_name
        
    def number_balanced_parenthesis(self, input_text: str, brace_type: str):
        # TODO - use recursive regular expressions
        assert brace_type in ['square', 'curly', 'circle']
        if brace_type == 'square':
            opening_brace = '['
            closing_brace = ']'
        elif brace_type == 'curly':
            opening_brace = '{'
            closing_brace = '}'
        else:
            opening_brace = '('
            closing_brace = ')'
        
        balanced_count = 0
        open_count = 0
        for character in input_text:
            if character == opening_brace:
                open_count += 1
            elif character == closing_brace:
                if open_count > 0:
                    balanced_count += 1
                    open_count -= 1
        return balanced_count
    
    def is_all_caps(self, token: str):
        token = token.strip()
        token = re.sub(r'[^\w\s]', '', token)
        return token.isalpha() and token == token.upper() and len(token) >= 3
    
    def number_camel_cased_tokens(self, token: str):
        def is_camel_case(token):
            if token != token.lower() and token != token.upper() and "_" not in token and sum(_ch.isupper() for _ch in token[1:-1]) >= 1:
                return True
            return False
        token = token.strip()
        cnt_camel_cased_tokens = 0
        punctuation_splitter = re.compile(r'[\s{}]+'.format(re.escape(punctuation)))
        for _token in punctuation_splitter.split(token):
            if is_camel_case(_token):
                cnt_camel_cased_tokens += 1
        return cnt_camel_cased_tokens
    
    def number_snake_cased_tokens(self, token: str):
        def is_snake_case(token):
            if "_" in token and (token == token.lower() or token == token.upper()):
                return True
            return False
        token = token.strip()
        cnt_snake_cased_tokens = 0
        punctuation_splitter = re.compile(r'[\s{}]+'.format(re.escape(punctuation.replace('_',''))))
        for _token in punctuation_splitter.split(token):
            if is_snake_case(_token):
                cnt_snake_cased_tokens += 1
        return cnt_snake_cased_tokens
    
    def heurestic(self, vector, threshold: int=4):
        return np.count_nonzero(vector) >= threshold
    
    def predict_log(self, documents: List[str]) -> List[bool]:
        """
        Predict if list of documents are logs or not
        """
        def _get_model_from_s3():
            try:
                s3_client = boto3.client('s3')
                response = s3_client.get_object(Bucket=self.model_s3_bucket, Key=self.model_s3_key)
                response_body = response['Body'].read()
                model = pickle.loads(response_body)
            except Exception:
                raise RuntimeError("Error occurred while getting log classification model from s3.")
            return model
            
        _document_vectors = []
        for document in documents:
            _document_vectors.append(self.parse(document))
        _documents_df = pd.DataFrame(_document_vectors, columns=['1', '2', '3', '4', '5', '6', '7', '8', '9'])
        classification_model = _get_model_from_s3()
        predictions = classification_model.predict(_documents_df)
        predictions = [round(_value) for _value in predictions]
        return [True if _a==1 else False for _a in predictions]

