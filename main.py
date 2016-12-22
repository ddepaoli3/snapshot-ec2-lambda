#!/usr/bin/env python

import boto3
import os

region = 'eu-west-1'

botosession = boto3.session.Session(region_name=region)
try:
    aws_secret_key = os.environ['AWS_SECRET_ACCESS_KEY']
    aws_access_key = os.environ['AWS_ACCESS_KEY_ID']
except Exception as e:
    print "Set AWS_SECRET_ACCESS_KEY and AWS_ACCESS_KEY_ID env"
    sys.exit(-1)

client = boto3.client('ec2')
print client.describe_volumes()