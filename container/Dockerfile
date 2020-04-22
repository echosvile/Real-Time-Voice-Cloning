FROM pytorch/pytorch:1.4-cuda10.1-cudnn7-runtime

RUN apt-get clean \
        && apt-get update \
        && apt-get install -y \
        ffmpeg \
        libportaudio2 \
        nginx 

# Install dependencies
RUN mkdir /opt/program 
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

ENTRYPOINT ["python", "server_wrapper.py"]