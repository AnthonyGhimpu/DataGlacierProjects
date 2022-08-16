import logging
import os
import subprocess
import yaml
import pandas as pd
import datetime 
import gc
import re

def readConfigFile(file):
    with open(file,'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as error:
            return logging.error(error)

def replacer(string, char):
    pattern = char +'{2,}'
    string = re.sub(pattern,char, string)
    return string

def col_header_val(df,table_config):
    df.columns = df.columns.str.lower()
    df.columns = df.columns.str.replace('[^\w]','_',regex = True)
    df.columns = list(map(lambda x: x.strip('_'),list(df.columns)))
    df.columns = list(map(lambda x: replacer(x,'_'),list(df.columns)))
    expected_col = list(map(lambda x: x.lower(),list(table_config['columns'])))
    expected_col.sort()
    df.columns = list(map(lambda x: x.lower(),list(df.columns)))
    df = df.reindex(sorted(df.columns),axis=1)

    if len(df.columns) == len(expected_col) and list(expected_col) == list(df.columns):
        print('Col names and col len validation passed')
        return 1
    else:
        print('Col names and col len validation failed')
        mismatched_col_file = list(set(df.columns).difference(expected_col))
        print('The following cols are not in the YAML File',mismatched_col_file)
        missing_YAML = list(set(expected_col).difference(df.columns))
        print('Following YAML cols are not in the file',missing_YAML)
        logging.info(f'df.columns:{df.columns}')
        logging.info(f'expected columns:{expected_col}')
        return 0
