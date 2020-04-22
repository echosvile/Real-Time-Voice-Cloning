"""Creates a SageMaker model using the image that we built"""

import boto3
import sagemaker as sage
from sagemaker import get_execution_role
import sys


def main(bucket_name, image_name):
    role = get_execution_role()
    sess = sage.Session()
    account = sess.boto_session.client('sts').get_caller_identity()['Account']
    region = sess.boto_session.region_name
    image = f'{account}.dkr.ecr.{region}.amazonaws.com/{image}:latest'
    mod = sage.model.Model(f's3://{bucket_name}/pretrained.tar.gz',
                           image,
                           name='voice-cloning-recall',
                           role=role)


if __name__ == 'main':
    if len(sys.argv) != 3:
        print('Usage: python create_model.py <bucket> <image>')
    else:
        main(sys.argv[1], sys.argv[2])
