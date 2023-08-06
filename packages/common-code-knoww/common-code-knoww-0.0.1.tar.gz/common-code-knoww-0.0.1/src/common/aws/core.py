import os

import boto3

session = boto3.session.Session()
region_name = os.environ.get('region')
