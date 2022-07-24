import logging
import sys
import yaml
import json
import argparse

def create_logger():
    # create logger
    logger = logging.getLogger('main')
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    return logger

def write_file(data,file_path,format):
    if format == 'yaml':
        with open(file_path, 'w+') as f:
            yaml.dump(data, f)
    elif format == 'json':
        with open(file_path, 'w+') as f:
            json.dump(data, f, indent=4)

def parse_args():
    parser = argparse.ArgumentParser(description='Generate Configs')
    parser.add_argument('-f', '--format', help="format for config output", choices=['yaml','json'], default='json')
    parser.add_argument('-n', '--name', help="output file name, without extension", default='lab_config')

    args = parser.parse_args()
    
    return args

