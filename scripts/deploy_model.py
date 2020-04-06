import boto3
import sagemaker as sage
from sagemaker import get_execution_role
import sys


def main(bucket_name):
    role = get_execution_role()
    sess = sage.Session()
    account = sess.boto_session.client('sts').get_caller_identity()['Account']
    region = sess.boto_session.region_name
    image = f'{account}.dkr.ecr.{region}.amazonaws.com/real-time-voice-cloning:latest'
    mod = sage.model.Model(f's3://{bucket_name}/pretrained.tar.gz',
                           image,
                           name='voice-cloning-recall',
                           role=role)

    mod.deploy(1, 'ml.p2.xlarge')


if __name__ == 'main':
    if len(sys.argv) != 2:
        print('Need an S3 bucket name...')
    else:
        main(sys.argv[1])
