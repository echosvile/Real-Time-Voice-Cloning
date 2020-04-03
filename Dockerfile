FROM pytorch/manylinux-cuda100


# Update install a sound library
RUN apt-get clean \
        && apt-get update \
        && apt-get install -y \
        ffmpeg \
        libportaudio2

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

# Install dependencies
WORKDIR /opt/program/
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "demo_cli.py", "--no_sound"]
#CMD ["nvcc", "--version"]