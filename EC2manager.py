#!/usr/bin/env python

from boto3 import Session
import boto3
import datetime


class EC2manager(Session):
    def __init__(self, *args, **kwargs):
        super(EC2manager, self).__init__(*args, **kwargs)
        self.ec2_service = self.resource('ec2')
        self.session = boto3.Session(**kwargs)
        self.ec2_client = self.session.client(service_name='ec2')

    def create_ami_all_instances(self):
        for i in self.ec2_service.instances.all():
            today = datetime.date.today()
            date = str(today)
            image_name = i.id + '-' +  date
            i.create_image(Name=image_name, InstanceId=i.id )

    def get_all_ami(self):
        output = self.ec2_client.describe_images(Owners=['self'])["Images"]
        return output

    def remove_ami(self, ami_id):
        all_ami_list = self.get_all_ami()
        for ami in all_ami_list:
            if ami["ImageId"] == ami_id:
                device_list = []
                for device in ami["BlockDeviceMappings"]:
                    try:
                        device_list.append(device["Ebs"]["SnapshotId"])
                    except Exception:
                        pass
        output = self.ec2_client.deregister_image(ImageId=ami_id)
        print "AMI " + ami_id + " removed"
        for snapshot in device_list:
             self.ec2_client.delete_snapshot(SnapshotId=snapshot)
             print "Snapshot " + snapshot + " removed"