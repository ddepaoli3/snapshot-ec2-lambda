#!/usr/bin/env python

import os
import sys
import datetime
from EC2manager import EC2manager

region = 'eu-west-1'
use_iam_role = False

def main():
    try:
        if use_iam_role:
            ec2_manager = EC2manager()
        else:
            aws_access_key_id = os.environ['AWS_SECRET_ACCESS_KEY']
            aws_secret_access_key = os.environ['AWS_ACCESS_KEY_ID']
            ec2_manager = EC2manager(aws_secret_access_key=aws_secret_access_key, aws_access_key_id=aws_access_key_id)
    except Exception as e:
        print "Set AWS_SECRET_ACCESS_KEY and AWS_ACCESS_KEY_ID env or set IAM role to instance that execute this script"
        sys.exit(-1)

    print ec2_manager.get_all_ami()


if __name__ == '__main__':
    main()