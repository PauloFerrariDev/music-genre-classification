import numpy as np
from librosa import feature
import time
import filter
from create_csv import create_csv_file

n_mfcc=20
playlist_size=30
singers = [
  "elza-soares", # samba
  "rita-lee", # mpb
  "roberta-miranda", # sertanejo
  "roberta-sa", # samba
  "cassia-eller", # rock
  "racionais-mcs", # rap
  "raimundos", # rock
  "planet-hemp", # hip-hop
  "natiruts", # reggae
  "jorge-ben-jor", # bossa nova
]

def bpm(audio, sr):
    bpm = feature.tempo(y=audio, sr=sr)[0]
    return bpm

def stft(audio, sr):
    y = feature.chroma_stft(y=audio, sr=sr)
    m = np.mean(y)
    v = np.var(y)
    return m, v

def cqt(audio, sr):
    y = feature.chroma_cqt(y=audio, sr=sr)
    m = np.mean(y)
    v = np.var(y)
    return m, v

def cens(audio, sr):
    y = feature.chroma_cens(y=audio, sr=sr)
    m = np.mean(y)
    v = np.var(y)
    return m, v

def contrast(audio, sr):
    y = feature.spectral_contrast(y=audio, sr=sr)
    m = np.mean(y)
    v = np.var(y)
    return m, v

def centroid(audio, sr):
    y = feature.spectral_centroid(y=audio, sr=sr)[0]
    m = np.mean(y)
    v = np.var(y)
    return m, v

def bandwidth(audio, sr):
    y = feature.spectral_bandwidth(y=audio, sr=sr)[0]
    m = np.mean(y)
    v = np.var(y)
    return m, v

def melspectrogram(audio, sr):
    y = feature.melspectrogram(y=audio, sr=sr)[0]
    m = np.mean(y)
    v = np.var(y)
    return m, v

def rms(audio):
    y = feature.rms(y=audio)[0]
    m = np.mean(y)
    v = np.var(y)
    return m, v

def mfcc(audio, sr):
    y = feature.mfcc(y=audio, sr=sr, n_mfcc=n_mfcc)
    m = np.mean(y, axis=1)
    v = np.var(y, axis=1)
    return m, v

#* CREATE MEAN AND VAR COLUMNS HEADER FOR EACH FEATURE
def create_data_table_header():
    header = ['singer','filename','sample','bpm','stft_mean','stft_var','cqt_mean','cqt_var','cens_mean','cens_var','contrast_mean','contrast_var','centroid_mean','centroid_var','bandwidth_mean','bandwidth_var','melspectrogram_mean','melspectrogram_var','rms_mean','rms_var']
    for i in range(1, n_mfcc+1):
        header = np.append(header, ['mfcc%s_mean'%i, 'mfcc%s_var'%i])
    return header

#* CREATE MEAN AND VAR COLUMNS FOR EACH FEATURE
def create_instance(singer, num_audio, sample, audio, sr):
    filename = "%s/audio-%s.wav"%(singer, num_audio)
    instance = np.array([singer,filename,sample,bpm(audio,sr),*stft(audio,sr),*cqt(audio,sr),
                         *cens(audio,sr),*contrast(audio,sr),*centroid(audio,sr),
                         *bandwidth(audio,sr),*melspectrogram(audio,sr),*rms(audio)])
    m, v = mfcc(audio,sr)
    for i in range(0, n_mfcc):
        instance = np.append(instance, [m[i], v[i]])
    return instance

#* CREATE MEAN AND VAR COLUMNS FOR EACH FEATURE
def get_audio_features(audio, sr):
    features = np.array([bpm(audio,sr),*stft(audio,sr),*cqt(audio,sr),
                         *cens(audio,sr),*contrast(audio,sr),*centroid(audio,sr),
                         *bandwidth(audio,sr),*melspectrogram(audio,sr),*rms(audio)])
    m, v = mfcc(audio,sr)
    for i in range(0, n_mfcc):
        features = np.append(features, [m[i], v[i]])
    return features

def run_features_script():
    print("\n*** START ***")
    # Record the start time
    start_time = time.time()
    header = create_data_table_header()
    csvfile, writer = create_csv_file("dataset_complete_2.csv")
    writer.writerow(header)          
    for singer in singers:
        singer_dir = "./audios/%s"%singer
        for num in range(0, playlist_size):
            audio_path = "%s/audio-%s.wav"%(singer_dir, num)
            print(audio_path)
            audio, sr, _ = filter.audio_data(audio_path)
            audio_lpf, *_ = filter.lowpass_filter(audio, sr)
            audio_bpf, *_ = filter.bandpass_filter(audio, sr)
            audio_hpf, *_ = filter.highpass_filter(audio, sr)
            audio_uniform_noise = filter.add_uniform_noise(audio, noise_level=0.09)
            audio_normal_noise = filter.add_normal_noise(audio, noise_level=0.09)
            uniform_noise_bpf, *_ = filter.bandpass_filter(audio_uniform_noise, sr)
            normal_noise_bpf, *_ = filter.bandpass_filter(audio_normal_noise, sr)
            instances = [create_instance(singer, num, 'original', audio, sr),
                        create_instance(singer, num, 'lowpass', audio_lpf, sr),
                        create_instance(singer, num, 'bandpass', audio_bpf, sr),
                        create_instance(singer, num, 'highpass', audio_hpf, sr),
                        create_instance(singer, num, 'uniform_noise', audio_uniform_noise, sr),
                        create_instance(singer, num, 'normal_noise', audio_normal_noise, sr),
                        create_instance(singer, num, 'uniform_noise_bandpass', uniform_noise_bpf, sr),
                        create_instance(singer, num, 'normal_noise_bandpass', normal_noise_bpf, sr),
                        ]
            for instance in instances:
                writer.writerow(instance)
    csvfile.close()
    # Record the end time
    end_time = time.time()
    # Calculate the elapsed time
    elapsed_time = end_time - start_time
    # Print the elapsed time
    print(f"Elapsed time: {elapsed_time} seconds")
    print("*** END ***\n")
            
#* Run script
#run_features_script()