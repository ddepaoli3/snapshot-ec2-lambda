#!/usr/bin/env python

import boto3
import os
import sys

region = 'eu-west-1'
use_iam_role = False

try:
    if use_iam_role:
        client = boto3.client('ec2')
    else:
        aws_access_key_id = os.environ['AWS_SECRET_ACCESS_KEY']
        aws_secret_access_key = os.environ['AWS_ACCESS_KEY_ID']
        client = boto3.client('ec2', aws_secret_access_key=aws_secret_access_key, aws_access_key_id=aws_access_key_id)
except Exception as e:
    print "Set AWS_SECRET_ACCESS_KEY and AWS_ACCESS_KEY_ID env or set IAM role to instance that execute this script"
    sys.exit(-1)

print client.describe_volumes()