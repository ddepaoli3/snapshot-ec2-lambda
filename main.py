#!/usr/bin/env python

from boto3 import Session
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

class EC2manager(Session):
    def __init__(self, *args, **kwargs):
        super(EC2manager, self).__init__(*args, **kwargs)
        self.ec2_service = self.resource('ec2')

    def create_ami_all_instances(self):
        for i in self.ec2_service.instances.all():
            today = datetime.date.today()
            date = str(today)
            image_name = i.id + '-' +  date
            i.create_image(Name=image_name, InstanceId=i.id )

    def get_all_ami(self):
        ec2_client = session.client(service_name='ec2')
        output = ec2_client.describe_images(Owners=['self'])["Images"]
        return output

if __name__ == '__main__':
    ec2_manager = EC2manager(aws_secret_access_key=aws_secret_access_key, aws_access_key_id=aws_access_key_id)
    print ec2_manager.get_all_ami()