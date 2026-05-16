import boto3
import urllib.parse
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3', endpoint_url=f"http://{os.environ.get('LOCALSTACK_HOSTNAME', 'localhost')}:4566")

def lambda_handler(event, context):
    try:
        source_bucket = event['Records'][0]['s3']['bucket']['name']
        object_key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
        target_bucket = os.environ.get('TARGET_BUCKET', 's3-finish')
        
        logger.info(f"Copying {object_key} from {source_bucket} to {target_bucket}")
        
        s3.copy_object(
            Bucket=target_bucket,
            Key=object_key,
            CopySource={'Bucket': source_bucket, 'Key': object_key}
        )
        
        logger.info("Copy successful")
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Error: {e}")
        raise e