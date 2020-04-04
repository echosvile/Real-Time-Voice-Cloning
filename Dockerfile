FROM pytorch/pytorch:1.4-cuda10.1-cudnn7-runtime

RUN apt-get clean \
        && apt-get update \
        && apt-get install -y \
        ffmpeg \
        libportaudio2 \
        nginx 

# TODO: remove all this once local tests are finished 
# Create the folder structure for sagemaker
RUN mkdir /opt/program \
        && mkdir /opt/ml \
        && mkdir /opt/ml/input \
        && mkdir /opt/ml/input/config \
        && mkdir /opt/ml/input/data \
        && mkdir /opt/ml/model \
        && mkdir /opt/ml/code \
        && mkdir /opt/ml/output \
        && mkdir /opt/ml/failure

# copy the model files
RUN pip install gdown
RUN gdown https://drive.google.com/uc?id=1n1sPXvT34yXFLT47QZA6FIRGrwMeSsZc
RUN apt-get install -y zip unzip
RUN unzip pretrained.zip -d /opt/ml/model
 
# Install dependencies
WORKDIR /opt/program/
COPY *.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy our source files
COPY *.py ./
COPY nginx.conf ./
COPY ./encoder ./encoder
COPY ./synthesizer ./synthesizer
COPY ./utils ./utils
COPY ./vocoder ./vocoder

#ENTRYPOINT ["python", "demo_cli.py", \
#            "--no_sound", \
#            "-e", "/opt/ml/model/encoder/saved_models/pretrained.pt", \
#            "-s", "/opt/ml/model/synthesizer/saved_models/logs-pretrained/", \
#            "-v", "/opt/ml/model/vocoder/saved_models/pretrained/pretrained.pt"]

ENTRYPOINT ["python", "service_wrapper.py"]