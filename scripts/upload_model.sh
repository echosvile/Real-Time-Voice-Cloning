my_bucket=real-time-voice-cloning

echo "Installing gdown..."
pip install gdown

echo "Downloading models..."
gdown https://drive.google.com/uc?id=1n1sPXvT34yXFLT47QZA6FIRGrwMeSsZc

echo "Repackaging models..."
unzip pretrained.zip
tar -czvf pretrained.tar.gz encoder synthesizer vocoder
rm -r encoder synthesizer vocoder
rm pretrained.zip

echo "Adding to S3..."
aws s3 mv pretrained.tar.gz s3://$my_bucsket/