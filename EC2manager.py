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

    def create_ami_all_instances(self, tags=[{'Key': 'CreatedByBackupScript','Value': 'true'}]):
        today = datetime.date.today()
        date = str(today)
        for instance in self.ec2_service.instances.all():
            try:
                instance_name = self.get_instance_name(instance.id)
                image_name =  instance_name + '-' + instance.id + '-' +  date
            except Exception:
                image_name = instance.id + '-' +  date
            print image_name
            output = instance.create_image(Name=image_name, InstanceId=instance.id, NoReboot=True )
            self.ec2_client.create_tags(Resources=[output.id], Tags=tags)

    def get_instance_name(self, instance_id):
        for instance in self.ec2_service.instances.all():
            if instance.id == instance_id:
                tags = instance.tags
                for tag in tags:
                    if tag["Key"] == "Name":
                        return tag["Value"]
        raise Exception("Name not value")

    def get_all_ami(self, filters=[{"Name":"tag-key", "Values":["CreatedByBackupScript"]}]):
        output = self.ec2_client.describe_images(Owners=['self'], Filters=filters)["Images"]
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

