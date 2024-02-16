import boto3

# Define EC2 client
ec2 = boto3.client('ec2')

# Launch an EC2 instance
response = ec2.run_instances(
    ImageId='ami-0c7217cdde317cfec',  # Replace 'ami-xxxxxxxx' with your desired AMI ID
    InstanceType='t3.nano',  # Choose instance type
    MinCount=1,
    MaxCount=1,
    KeyName='My_EC2_Key',  # Replace 'your-key-pair' with your key pair name
    SecurityGroupIds=['sg-0a244911c1c483637'],  # Replace 'your-security-group-id' with your security group ID

    UserData='''#!/bin/bash
                sudo apt update -y
                sudo apt install nginx -y
                cd /var/www/html
                sudo rm -rf index.nginx-debian.html 
                echo "<html><h1>Hello from your EC2 web server 2 with Nginx</h1></html>" > index.html
                sudo systemctl restart nginx
                '''
            
)

# Get the instance ID
instance_id = response['Instances'][0]['InstanceId']
print("Instance ID:", instance_id)
