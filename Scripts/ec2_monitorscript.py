import boto3
from datetime import datetime

ec2 = boto3.client('ec2', region_name='eu-south-1')

def start_instance(instance_id):
    ec2.start_instances(InstanceIds=[instance_id])
    print(f"Started instance: {instance_id}")

def stop_instance(instance_id):
    ec2.stop_instances(InstanceIds=[instance_id])
    print(f"Stopped instance: {instance_id}")

def schedule_instance(instance_id):
    current_time = datetime.now()
    # Check if current time is between 19:50 PM and 19:55 PM
    if current_time.hour == 19 and current_time.minute == 50:
        start_instance(instance_id)
    elif current_time.hour == 19 and current_time.minute == 55:
        stop_instance(instance_id)
    else:
        print("Instance is not scheduled to start or stop at this time.")

def check_instance_state(instance_id):
    # Describe the instance to get its state
    response = ec2.describe_instances(InstanceIds=[instance_id])

    # Extract the instance state
    instance_state = response['Reservations'][0]['Instances'][0]['State']['Name']

    # Check if the instance is stopped and print a custom message
    if instance_state == 'stopped':
        print(f"The instance {instance_id} is currently STOPPED. Check CloudWatch Alarm and do the needed the instance to proceed.")
    else:
        print(f"The instance {instance_id} is currently {instance_state.upper()}.")

# Example usage
instance_id = "i-06a76716ea64da877"  # Replace with your actual instance ID

# Check the current state of the instance
check_instance_state(instance_id)

# Schedule the instance based on time
schedule_instance(instance_id)
