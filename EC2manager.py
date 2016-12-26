#!/usr/bin/env python

from boto3 import Session
import boto3
import datetime


class EC2manager(Session):
    '''
    Class use to personal manage of ec2 resources.
    It is inheritance from Session
    '''
    def __init__(self, *args, **kwargs):
        '''
        Init class. Take argument from Session boto3 class
        (http://boto3.readthedocs.io/en/latest/reference/core/session.html)
        '''
        super(EC2manager, self).__init__(*args, **kwargs)
        self.ec2_service = self.resource('ec2')
        self.session = boto3.Session(**kwargs)
        self.ec2_client = self.session.client(service_name='ec2')

    def create_ami_all_instances(self, tags=[{'Key': 'CreatedByBackupScript','Value': 'true'}]):
        '''
        Create AMI from all instances in the account

        Args:
            tags (list): list of tags to applied to create ami
        '''
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
        '''
        Get the instance name from tags Name

        Args:
            instance_id (string): id of the instance from which obtain the Name

        Returns:
            Name (string): return the string name or raise expcetion if no tag name is found
        '''
        for instance in self.ec2_service.instances.all():
            if instance.id == instance_id:
                tags = instance.tags
                for tag in tags:
                    if tag["Key"] == "Name":
                        return tag["Value"]
        raise Exception("Name not value")

    def get_all_ami(self, filters=[{"Name":"tag-key", "Values":["CreatedByBackupScript"]}]):
        '''
        Get all ami present in the account

        Args:
            filter (list): Filters to be used to reduce len of ami.

        Returns:
            ami_list (list): list of ami filtered. By default only ami with tag CreatedByBackupScript are returned
        '''
        output = self.ec2_client.describe_images(Owners=['self'], Filters=filters)["Images"]
        return output

    def remove_ami(self, ami_id):
        '''
        Remove a given ami and snapshot related to it

        Args:
            ami_id (string): id of the ami to remove
        '''
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

