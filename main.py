#!/usr/bin/env python

import os
import sys
import datetime
from datetime import datetime, timedelta
from EC2manager import EC2manager

region = 'eu-west-1'
use_iam_role = False

try:
    if use_iam_role:
        ec2_manager = EC2manager()
    else:
        aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
        aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
        ec2_manager = EC2manager(aws_secret_access_key=aws_secret_access_key, aws_access_key_id=aws_access_key_id)
except Exception as e:
    print "Set AWS_SECRET_ACCESS_KEY and AWS_ACCESS_KEY_ID env or set IAM role to instance that execute this script"
    sys.exit(-1)

def delete_older_than_given_days(days):
    delete_time = datetime.utcnow() - timedelta(days=days)
    for ami in ec2_manager.get_all_ami():
        created_ami_time = datetime.strptime(ami['CreationDate'], '%Y-%m-%dT%H:%M:%S.000Z')
        if created_ami_time < delete_time:
            print "da cancellare ami " + ami["ImageId"]
            ec2_manager.remove_ami(ami["ImageId"], DryRun=True)

def remove_filered():
    for ami in ec2_manager.get_all_ami(Filters=[{"Name":"tag-key", "Values":["CreatedByBackupScript"]},{'Name':'tag:versione', 'Values':['2']}]):
        ec2_manager.remove_ami(ami["ImageId"], DryRun=False)

def main():
    pass
    #ec2_manager.create_ami_all_instances()
    #print ec2_manager.get_all_ami()
    #ec2_manager.remove_ami("ami-efc8eb9c")



if __name__ == '__main__':
    delete_older_than_given_days(0)
    ec2_manager.create_ami_all_instances(DryRun=True, Filters=[{'Name':'tag:Name', 'Values':['verisure-LMS-Collaudo']}])
    print ec2_manager.get_all_ami(Filters=[{"Name":"tag-key", "Values":["CreatedByBackupScript"]},{'Name':'tag:versione', 'Values':['2']}])
    #delete_older_than_given_days(0)