import boto3

ec2 = boto3.client('ec2', region_name='eu-south-1')

def start_instance(instance_id):
    ec2.start_instances(InstanceIds=[instance_id])
    print(f"Started instance: {instance_id}")

def stop_instance(instance_id):
    ec2.stop_instances(InstanceIds=[instance_id])
    print(f"Stopped instance: {instance_id}")

# Example Usage
INSTANCE_ID = "i-0d63c89c1260dafd6"
start_instance(INSTANCE_ID)
stop_instance(INSTANCE_ID)


import boto3
from botocore.exceptions import NoCredentialsError

ec2 = boto3.client('ec2', region_name='eu-south-1')
sns = boto3.client('sns', region_name='eu-south-1')

def start_instance(instance_id):
    try:
        ec2.start_instances(InstanceIds=[instance_id])
        print(f"Started instance: {instance_id}")
    except NoCredentialsError:
        print("Credentials not available")

def stop_instance(instance_id):
    try:
        ec2.stop_instances(InstanceIds=[instance_id])
        print(f"Stopped instance: {instance_id}")
    except NoCredentialsError:
        print("Credentials not available")

def send_alert(topic_arn, message):
    try:
        sns.publish(TopicArn=topic_arn, Message=message)
        print("Alert sent!")
    except Exception as e:
        print(f"Error sending alert: {e}")

# Example Usage
INSTANCE_ID = "i-0d63c89c1260dafd6"
TOPIC_ARN = "arn:aws:sns:eu-south-1:788231899881:Default_CloudWatch_Alarms_Topic"

# Start or stop instances as needed
start_instance(INSTANCE_ID)
stop_instance(INSTANCE_ID)

# Send an alert
send_alert(TOPIC_ARN, "EC2 instance stopped due to high CPU usage!")


