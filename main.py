#!/usr/bin/env python

import boto3
import os
import sys
import datetime


region = 'eu-west-1'
use_iam_role = False

try:
    if use_iam_role:
        session = boto3.Session()
        ec2 = session.resource('ec2')
    else:
        aws_access_key_id = os.environ['AWS_SECRET_ACCESS_KEY']
        aws_secret_access_key = os.environ['AWS_ACCESS_KEY_ID']
        session = boto3.Session(aws_secret_access_key=aws_secret_access_key, aws_access_key_id=aws_access_key_id)
        ec2 = session.resource('ec2')
except Exception as e:
    print "Set AWS_SECRET_ACCESS_KEY and AWS_ACCESS_KEY_ID env or set IAM role to instance that execute this script"
    sys.exit(-1)

for i in ec2.instances.all():
    today = datetime.date.today()
    date = str(today)
    image_name = i.id + '-' +  date
    i.create_image(Name=image_name, InstanceId=i.id )