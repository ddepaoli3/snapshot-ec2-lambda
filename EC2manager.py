#!/usr/bin/env python

from boto3 import Session
import boto3
import datetime


class EC2manager(Session):
    def __init__(self, *args, **kwargs):
        super(EC2manager, self).__init__(*args, **kwargs)
        self.ec2_service = self.resource('ec2')
        self.session = boto3.Session(**kwargs)

    def create_ami_all_instances(self):
        for i in self.ec2_service.instances.all():
            today = datetime.date.today()
            date = str(today)
            image_name = i.id + '-' +  date
            i.create_image(Name=image_name, InstanceId=i.id )

    def get_all_ami(self):
        ec2_client = self.session.client(service_name='ec2')
        output = ec2_client.describe_images(Owners=['self'])["Images"]
        return output

    def deregister_ami(self):
        pass