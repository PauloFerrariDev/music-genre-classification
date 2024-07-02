#import os
import numpy as np
import joblib
import librosa
import features
from features import singers
import filter
from random import randint
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model

# Forçar TensorFlow a usar a CPU
#os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

######### LOAD MODEL #########
model = load_model('dataset_complete_with_recordings.h5')
scaler = joblib.load('scaler.pkl')
label_encoder = joblib.load('label_encoder.pkl')

def identify_singer(audio, sr):    
    audio_bpf, *_ = filter.bandpass_filter(audio, sr)
    # filter.play_audio(audio_bpf, sr)

    audio_features = features.get_audio_features(audio_bpf, sr)
    audio_features = audio_features.reshape(1, -1)

    # Padronizar as características usando o scaler salvo
    audio_features = scaler.transform(audio_features)

    # Fazer a predição usando o modelo de rede neural
    singer_predicted = model.predict(audio_features)
    print('singer_predicted', singer_predicted)
    singer_predicted_class = np.argmax(singer_predicted, axis=1)
    print('singer_predicted_class', singer_predicted_class)
    singer_predicted_label = label_encoder.inverse_transform(singer_predicted_class)
    print('singer_predicted_label', singer_predicted_label)
    
    print("Identified singer:", singer_predicted_label[0])

def run_singer_classifier_audios_script():
    for singer in singers:       
        num = randint(0, 29)
        audio_path = f"./audios/{singer}/audio-{num}.wav"
        print("Identifying the singer of:", audio_path)
        audio, sr = librosa.load(audio_path)
        identify_singer(audio, sr)

def run_singer_classifier_recording_script():
    duration = 30
    audio, sr = filter.record_audio(duration)
    audio = np.array(np.array(audio).flat) # essa linha está correta!
    audio = filter.audio_normalized(audio)

    print('Audio:', audio)
    print('Audio length:', len(audio))
    print('Audio sample rate:', sr)
    filter.play_audio(audio, sr, duration)
    identify_singer(audio, sr)

# run_singer_classifier_audios_script()
run_singer_classifier_recording_script()
