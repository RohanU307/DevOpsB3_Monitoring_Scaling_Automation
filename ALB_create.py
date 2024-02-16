import boto3

# Define the boto3 clients for ELB and EC2
elbv2 = boto3.client('elbv2')
ec2 = boto3.client('ec2')

# ALB params
alb_name = 'Rohan-ALB'
subnet_ids = ['subnet-022ea368e2afbf1c3', 'subnet-022498ed0aeab77b7']  
security_group_ids = ['sg-0a244911c1c483637']  
port = 80  

# Creating the ALB
response = elbv2.create_load_balancer(
    Name=alb_name,
    Subnets=subnet_ids,
    SecurityGroups=security_group_ids,
    Scheme='internet-facing',
)

alb_arn = response['LoadBalancers'][0]['LoadBalancerArn']

# Create a target group
target_group_name = 'Rohan-TG'
response = elbv2.create_target_group(
    Name=target_group_name,
    Protocol='HTTP',
    Port=port,
    VpcId='vpc-0006d3d20cacf95ed',  # Replace with your VPC ID
    TargetType='instance'
)
target_group_arn = response['TargetGroups'][0]['TargetGroupArn']

# Registering EC2 instances with the target group
instances = ['i-044226048685bcc43', 'i-09836de780167b919'] 
elbv2.register_targets(
    TargetGroupArn=target_group_arn,
    Targets=[
        {'Id': instance_id} for instance_id in instances
    ]
)
# Creating listener for the ALB
response = elbv2.create_listener(
    LoadBalancerArn=alb_arn,
    Protocol='HTTP',
    Port=port,
    DefaultActions=[
        {
            'Type': 'forward',
            'TargetGroupArn': target_group_arn
        },
    ]
)

print("ALB deployed successfully and EC2 instances registered.")
