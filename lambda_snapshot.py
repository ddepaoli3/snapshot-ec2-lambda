#!/usr/bin/env python

from flask import Flask
from EC2manager import EC2manager
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/')
def index():
    return "Snapshot Lambda app!", 200

@app.route('/ami')
def get_all_ami():
    try:
        ec2_manager = EC2manager()
        all_ami = str(ec2_manager.get_all_ami(Filters=[{"Name":"tag-key", "Values":["CreatedByBackupScript"]}]))
    except Exception:
        all_ami = "Error in get AMI list"
    return all_ami, 200

@app.route('/snapshotall')
def snapshot_all(event=None, context=None):
    try:
        ec2_manager = EC2manager()
        output = ec2_manager.create_ami_all_instances()
    except Exception:
        output = "Error. Impossible to snapshot instances"
    return str(output), 200

@app.route('/deleteolderthan/<days_num>')
def delete_older_than_given_days_api(event=None, context=None, days_num=0):
    try:
        ec2_manager = EC2manager()
    except Exception:
        return "Impossible to create ec2 session. Cannot continue", 200
    delete_time = datetime.utcnow() - timedelta(days=int(days_num))
    delete_ami_list = []
    for ami in ec2_manager.get_all_ami(Filters=[{"Name":"tag-key", "Values":["CreatedByBackupScript"]}]):
        created_ami_time = datetime.strptime(ami['CreationDate'], '%Y-%m-%dT%H:%M:%S.000Z')
        if created_ami_time < delete_time:
            ec2_manager.remove_ami(ami["ImageId"])
            delete_ami_list.append(ami["ImageId"])
    return str(delete_ami_list), 200

def delete_older_than_given_days(event=None, context=None):
    days_num=8
    try:
        ec2_manager = EC2manager()
    except Exception:
        return "Impossible to create ec2 session. Cannot continue", 200
    delete_time = datetime.utcnow() - timedelta(days=int(days_num))
    delete_ami_list = []
    for ami in ec2_manager.get_all_ami(Filters=[{"Name":"tag-key", "Values":["CreatedByBackupScript"]}]):
        created_ami_time = datetime.strptime(ami['CreationDate'], '%Y-%m-%dT%H:%M:%S.000Z')
        if created_ami_time < delete_time:
            ec2_manager.remove_ami(ami["ImageId"], DryRun=False)
            delete_ami_list.append(ami["ImageId"])
    return str(delete_ami_list), 200

if __name__ == '__main__':
    app.run()
