FROM pytorch/pytorch:1.4-cuda10.1-cudnn7-runtime

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
 
# Copy our source files
COPY *.py /opt/program/
COPY *.txt /opt/program/
COPY ./encoder /opt/program/encoder
COPY ./synthesizer /opt/program/synthesizer
COPY ./utils /opt/program/utils
COPY ./vocoder /opt/program/vocoder

# Install a sound library
RUN apt-get clean \
        && apt-get update \
        && apt-get install -y \
        ffmpeg \
        libportaudio2

# Install dependencies
WORKDIR /opt/program/
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "demo_cli.py", "--no_sound"]