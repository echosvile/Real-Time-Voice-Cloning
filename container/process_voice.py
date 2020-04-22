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
import os
import glob
import warnings


app = flask.Flask(__name__)
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

# Ok to hard code these locations
encoder_model_path = '/opt/ml/model/encoder/saved_models/pretrained.pt'
synthesizer_path = '/opt/ml/model/synthesizer/saved_models/logs-pretrained/taco_pretrained/'
vocoder_model_path = '/opt/ml/model/vocoder/saved_models/pretrained/pretrained.pt'

# Load the models
encoder.load_model(Path(encoder_model_path))
synthesizer = Synthesizer(Path(synthesizer_path))
vocoder.load_model(Path(vocoder_model_path))


def clone_voice(sentence, results_file):
    """Adapted from 'demo_cli.py'"""
    u_path = Path('utterance.wav')
    results_path = Path(results_file)
    
    preprocessed_wav = encoder.preprocess_wav(u_path)
    embed = encoder.embed_utterance(preprocessed_wav)
    specs = synthesizer.synthesize_spectrograms([sentence], [embed])
    generated_wav = vocoder.infer_waveform(specs[0])
    generated_wav = np.pad(generated_wav, (0, synthesizer.sample_rate), mode="constant")
    
    librosa.output.write_wav(results_path, generated_wav.astype(np.float32), 
                             synthesizer.sample_rate)
            

@app.route('/ping', methods=['GET'])
def ping():
    """Required by SageMaker to check the health of our container"""
    return flask.Response(response='\n', status=200, mimetype='application/json')


@app.route('/invocations', methods=['POST'])
def transformation():
    """The main route where we process requests"""
    if flask.request.content_type != 'application/json':
        return flask.Response(response='Input should be application/json', status=415, mimetype='text/plain')

    data = flask.request.get_json()
    app.logger.warn(f'Starting request: {data["request_id"]}...')
    
    if data['request_type'] == 'batch_processing':
        s3 = boto3.client('s3')
        
        for job in data['jobs']:
            job_id = job['job_id']
            app.logger.info(f'Starting job: f{job_id}...')
            
            # Download the utterance file
            s3.download_file(job['bucket'], job['utterance_file'], 'utterance.wav')
            
            idx = 0
            for sentence in job['sentences']:
                # Generate and upload a .wav file for each sentence in the job
                app.logger.info(f'Processing sentence {idx} of job {job_id}...')
                results_file = f'{job_id}_{idx}.wav'
                clone_voice(sentence, results_file)
                s3.upload_file(results_file, job['bucket'], results_file)
                idx += 1
            
            # Clean up
            wav_files = glob.glob('./*.wav')
            for file in wav_files:
                os.remove(file)
                            
        return flask.Response(response='Job complete!', status=200, mimetype='application/json')
    else:
        return flask.Response(response=f'Unrecognized request_type: {data["request_type"]}',
                              status=400, mimetype='text/plain')