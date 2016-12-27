#!/usr/bin/env python

from flask import Flask
from EC2manager import EC2manager

app = Flask(__name__)

@app.route('/')
def index():
    return "Snapshot Lambda app!", 200

@app.route('/ami')
def get_all_ami():
    try:
        ec2_manager = EC2manager()
        all_ami = str(ec2_manager.get_all_ami())
    except Exception:
        all_ami = "Error in get AMI list"
    return all_ami, 200

@app.route('/snapshotall')
def snapshot_all():
    try:
        ec2_manager = EC2manager()
        output = ec2_manager.create_ami_all_instances()
    except Exception:
        output = "Error. Impossible to snapshot instances"
    return str(output), 200

if __name__ == '__main__':
    app.run()
