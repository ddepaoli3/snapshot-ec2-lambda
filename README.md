README
======

# Introduction
This repository contains a tool to create backup of ec2 resources in an ami format and delete them.
It is written in python with boto3 library and is runnable in aws lambda or standalone.

# Description
The main class in __EC2manager__ defined in _EC2manager.py_ and it derived from boto3 Session class. It is just a overhead class used to manage the resources by the script.
In _main.py_ there is an example of how to use the script. In _lambda_snapshot.py_ the main file to use with lambda.

The script associates with the created AMI a tag (_CreatedByBackupScript_) that is used as filter when remove the AMI. Be sure to filter

# Standalone script
To work with standalone script you have to use your API access and secret key. Export it as:
```
export AWS_ACCESS_KEY_ID=<your_access_key>
export AWS_SECRET_ACCESS_KEY=<your_secret_key>
```
If the script is executed inside an ec2 with IAM role able to create AMI set use_iam_role as True and no access and secret key are needed.

# Lambda script

## IAM role for lambda
To correctly execute the lambda it needs the permission to access EC2. The default role create by zappa is not sufficient for this purpose.
In folder _cloudformation_ there is a template that create a single role that can be associated with lambda.
To launch template:
```
aws cloudformation create-stack --profile profile_na,e --stack-name snapshot-lambda-role --template-body file://lamda-role-cloudformation.yml --capabilities CAPABILITY_IAM --capabilities CAPABILITY_NAMED_IAM
```
The new role is called _SnapshotLambdaRole_

## Deploy code with lambda
Lambda script is deployed on AWS using [zappa](https://github.com/Miserlou/Zappa). Using a new python virtual environment install all dependencies with:
```
pip install -r requirements.txt
```

In _zappa_settings.json_ are defined 3 application:
* __SnapshotApi__: rest api AMI creation and delete. It creates API gateway for API management.
* __CreateAmiCronApp__: application without API gateway schedules on cron expression. It creates the AMI
* __DeleteAmiCronApp__: application without API gateway schedules on cron expression. It deletes the AMI older than specified number of days. 
To change number of days set it as default value in _delete\_older\_than\_given\_days_ function

These parameters should be changed based on your configuration and preferences:
* _s3\_bucket_: name of the bucket to upload code to
* _aws\_region_: aws region
* _profile\_name_: profile name of your awscli configuration
* _role\_name_: name of the role to associate with lambda. It needs the permission to create AMI. For more details read subsection _IAM role for Lambda_
* _cron\_expression_: cron expression to use. [More details](http://docs.aws.amazon.com/lambda/latest/dg/tutorial-scheduled-events-schedule-expressions.html)

To deploy using zappa:
```
zappa deploy <application_name>
```

To update:
```
zappa update <application_name>
```