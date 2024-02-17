import boto3

ec2 = boto3.client('ec2')
autoscaling = boto3.client('autoscaling')

# EC2
instance_id = 'i-044226048685bcc43'
instance_type = 't3.nano'
key_name = 'My_EC2_Key'
security_group_ids = ['sg-0a244911c1c483637']
subnet_id = 'subnet-022ea368e2afbf1c3'
iam_instance_profile = 'EC2InstanceProfileForImageBuilder'

# Create a launch configuration
response = autoscaling.create_launch_configuration(
    LaunchConfigurationName='Rohan-launch-config',
    ImageId='ami-0c7217cdde317cfec',
    InstanceType=instance_type,
    KeyName=key_name,
    SecurityGroups=security_group_ids,
    IamInstanceProfile=iam_instance_profile,
)

# Creating an Auto Scaling group
response = autoscaling.create_auto_scaling_group(
    AutoScalingGroupName='Rohan-ASG',
    LaunchConfigurationName='Rohan-launch-config',
    MinSize=2,
    MaxSize=5,
    DesiredCapacity=2,
    AvailabilityZones=['us-east-1a', 'us-east-1a'],
    VPCZoneIdentifier=subnet_id,
)

response = autoscaling.put_scaling_policy(
    AutoScalingGroupName='Rohan-ASG',
    PolicyName='scale-out-policy',
    PolicyType='TargetTrackingScaling',
    TargetTrackingConfiguration={
        'PredefinedMetricSpecification': {
            'PredefinedMetricType': 'ASGAverageCPUUtilization'
        },
        'TargetValue': 90,
    }
)
response = autoscaling.put_scaling_policy(
    AutoScalingGroupName='Rohan-ASG',
    PolicyName='scale-in-policy',
    PolicyType='TargetTrackingScaling',
    TargetTrackingConfiguration={
        'PredefinedMetricSpecification': {
            'PredefinedMetricType': 'ASGAverageCPUUtilization'
        },
        'TargetValue': 20,
    }
)

print("Auto Scaling group and scaling policies created successfully.")
