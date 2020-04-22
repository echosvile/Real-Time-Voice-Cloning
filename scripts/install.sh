# Run this from either 1) a SageMaker notebook instance or 2) an AWS CLI with python and docker installed.

# Add your AWS resource names here: 
bucket_name=
ecr_repository_name=


if [ -z $bucket_name ] || [ -z $ecr_repository_name ] 
    then
      echo "You must provide an S3 bucket and Elastic Container Registry repository"
      exit
fi


echo "Installing gdown..."
pip install gdown

echo "Downloading models..."
gdown https://drive.google.com/uc?id=1n1sPXvT34yXFLT47QZA6FIRGrwMeSsZc

echo "Repackaging models..."
unzip pretrained.zip
tar -czvf pretrained.tar.gz encoder synthesizer vocoder
rm -r encoder synthesizer vocoder
rm pretrained.zip

echo "Adding model to S3..."
aws s3 mv pretrained.tar.gz s3://$bucket_name/

echo "Adding utterances to S3..."
aws s3 cp ../data/darth.mp3 s3://$bucket_name/
aws s3 cp ../data/ssre-normal.wav s3://$bucket_name/

echo "Signing into AWS ECR..."
account=$(aws sts get-caller-identity --query Account --output text)
region=$(aws configure get region)
fullname="${account}.dkr.ecr.${region}.amazonaws.com/${ecr_repository_name}:latest"

$(aws ecr get-login --region ${region} --no-include-email)

echo "Building image..."
docker build  -t ${ecr_repository_name} ../container
docker tag ${ecr_repository_name} ${fullname}

echo "Pushing image..."
docker push ${fullname}

echo "Creating SageMaker model..."
python create_model.py $bucket_name $ecr_repository_name
