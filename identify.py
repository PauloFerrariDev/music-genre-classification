import numpy as np
import joblib
import librosa
import features
from features import singers
import filter
from random import randint
import matplotlib.pyplot as plt

######### LOAD MODEL #########
SINGER_MODEL = joblib.load('singer_identifier_svm_linear_model.pkl')

def identify_singer(audio, sr):    
    audio_bpf, *_ = filter.bandpass_filter(audio, sr)
    filter.play_audio(audio_bpf, sr)

    # L = len(audio)
    # t = np.linspace(start=0, stop=L/sr, num=L) # samples
    # plt.subplot(2,1,1)
    # plt.plot(t,audio)
    # plt.subplot(2,1,2)
    # plt.plot(t,audio_bpf)
    # plt.show()

    audio_features = features.get_audio_features(audio_bpf, sr)
    audio_features = audio_features.reshape(1, -1)
    singer_predicted = SINGER_MODEL.predict(audio_features)
    print("Identified singer:", singer_predicted)

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
    audio = np.array(np.array(audio).flat) # essa linha esta correta!
    audio = filter.audio_normalized(audio)

    # L = len(audio)
    # t = np.linspace(start=0, stop=L/sr, num=L) # samples
    # plt.subplot(2,1,1)
    # plt.plot(t,audio)
    # plt.subplot(2,1,2)
    # plt.plot(t,audio_n)
    # plt.show()

    print('Audio:', audio)
    print('Audio length:', len(audio))
    print('Audio sample rate:', sr)
    filter.play_audio(audio, sr, duration)
    identify_singer(audio, sr)

# run_singer_classifier_audios_script()
run_singer_classifier_recording_script()
    