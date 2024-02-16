import boto3

bucket_name='rohanboto3bucket'
region_name='ap-south-1'


# Create an S3 client
s3 = boto3.client('s3',  region_name=region_name)

# Create the bucket
response = s3.create_bucket(
    Bucket=bucket_name,
    CreateBucketConfiguration={
        'LocationConstraint': region_name
    }
)

print(response)