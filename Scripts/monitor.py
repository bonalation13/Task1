import boto3
import pandas as pd
from datetime import datetime, timedelta

# Initialize AWS clients
ec2 = boto3.client('ec2', region_name='eu-south-1')  # Change region if needed
cloudwatch = boto3.client('cloudwatch', region_name='eu-south-1')

# Function to get CPU utilization for an instance
def get_cpu_utilization(instance_id):
    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
        StartTime=datetime.utcnow() - timedelta(days=1),  # Last 24 hours
        EndTime=datetime.utcnow(),
        Period=60,  # 1-min intervals
        Statistics=['Average']
    )
    datapoints = response['Datapoints']
    if datapoints:
        return sum(point['Average'] for point in datapoints) / len(datapoints)
    return 0

# Function to generate a report
def generate_report():
    instances = ec2.describe_instances()['Reservations']
    report_data = []

    for reservation in instances:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            instance_type = instance['InstanceType']
            state = instance['State']['Name']
            cpu_utilization = get_cpu_utilization(instance_id)

            recommendation = "No action needed"
            if cpu_utilization < 10:  # Underutilized
                recommendation = "Consider stopping or resizing the instance"

            report_data.append({
                'Instance ID': instance_id,
                'Instance Type': instance_type,
                'State': state,
                'CPU Utilization (%)': cpu_utilization,
                'Recommendation': recommendation
            })

    # Convert to DataFrame and save as CSV
    df = pd.DataFrame(report_data)
    df.to_csv('cloud_monitoring_report.csv', index=False)
    print("Report generated: cloud_monitoring_report.csv")

# Main function
if __name__ == "__main__":
    generate_report()
