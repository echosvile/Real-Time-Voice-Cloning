import flask
from encoder.params_model import model_embedding_size as speaker_embedding_size
from utils.argutils import print_args
from synthesizer.inference import Synthesizer
from encoder import inference as encoder
from vocoder import inference as vocoder
from pathlib import Path
import numpy as np
import librosa
import argparse
import torch
import boto3

app = flask.Flask(__name__)

# Ok to hard code these locations
encoder_model_path = '/opt/ml/model/encoder/saved_models/pretrained.pt'
synthesizer_path = '/opt/ml/model/synthesizer/saved_models/logs-pretrained/taco_pretrained/'
vocoder_model_path = '/opt/ml/model/vocoder/saved_models/pretrained/pretrained.pt'

# Load the models
encoder.load_model(Path(encoder_model_path))
synthesizer = Synthesizer(Path(synthesizer_path))
vocoder.load_model(Path(vocoder_model_path))


@app.route('/ping', methods=['GET'])
def ping():
    return flask.Response(response='\n', status=200, mimetype='application/json')


@app.route('/invocations', methods=['POST'])
def transformation():
    if flask.request.content_type != 'application/json':
        return flask.Response(response='Input should be application/json', status=415, mimetype='text/plain')

    data = flask.request.data.decode('utf-8')
    app.logger.warn("testing logger message...")
    return flask.Response(response='Hello from sagemaker!', status=200, mimetype='application/json')
