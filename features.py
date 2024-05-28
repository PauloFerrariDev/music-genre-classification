import numpy as np
from librosa import feature
import time
import filter
from create_csv import create_data_table_csv

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

# Coefficient of Variation (CV %)
def cv (y, axis=None):
    cv_arr = np.std(a=y, axis=axis) / np.mean(a=y, axis=axis) * 100 
    return np.round(a=cv_arr, decimals=5)

def tempo(audio, sr):
    return feature.tempo(y=audio, sr=sr)[0]

def stft(audio, sr):
    y = feature.chroma_stft(y=audio, sr=sr)
    return cv(y)

def cqt(audio, sr):
    y = feature.chroma_cqt(y=audio, sr=sr)
    return cv(y)

def cens(audio, sr):
    y = feature.chroma_cens(y=audio, sr=sr)
    return cv(y)

def contrast(audio, sr):
    y = feature.spectral_contrast(y=audio, sr=sr)
    return cv(y)

def centroid(audio, sr):
    y = feature.spectral_centroid(y=audio, sr=sr)[0]
    return cv(y)

def bandwidth(audio, sr):
    y = feature.spectral_bandwidth(y=audio, sr=sr)[0]
    return cv(y)

def melspectrogram(audio, sr):
    y = feature.melspectrogram(y=audio, sr=sr)[0]
    return cv(y)

def rms(audio):
    y = feature.rms(y=audio)[0]
    return cv(y)

def mfcc(audio, sr):
    y = feature.mfcc(y=audio, sr=sr, n_mfcc=n_mfcc)
    return cv(y, axis=1)

def create_data_table_header():
    header = ['singer','filename','sample','tempo','stft_cv','cqt_cv','cens_cv','contrast_cv','centroid_cv','bandwidth_cv','melspectrogram_cv','rms_cv']
    for i in range(1, n_mfcc+1):
        header = np.append(header, ['mfcc%s_cv'%i])
    return header

# def create_data_table_header():
#     header = ['singer','filename','tempo','stft_mean','stft_var','cqt_mean','cqt_var','cens_mean','cens_var','contrast_mean','contrast_var','centroid_mean','centroid_var','bandwidth_mean','bandwidth_var','melspectrogram_mean','melspectrogram_var','rms_mean','rms_var']
#     for i in range(1, n_mfcc+1):
#         header = np.append(header, ['mfcc%s_mean'%i, 'mfcc%s_var'%i])
#     return header

def create_instance(singer, num_audio, sample, audio, sr):
    filename = "%s/audio-%s.wav"%(singer, num_audio)
    instance = np.array([singer,filename,sample,tempo(audio,sr),stft(audio,sr),cqt(audio,sr),
                         cens(audio,sr),contrast(audio,sr),centroid(audio,sr),
                         bandwidth(audio,sr),melspectrogram(audio,sr),rms(audio)])
    cv = mfcc(audio,sr)
    for i in range(0, n_mfcc):
        instance = np.append(instance, [cv[i]])
    return instance

# def create_instance(singer, num_audio, audio, sr):
#     filename = "%s/audio-%s.wav"%(singer, num_audio)
#     instance = np.array([singer,filename,tempo(audio,sr),*stft(audio,sr),*cqt(audio,sr),
#                          *cens(audio,sr),*contrast(audio,sr),*centroid(audio,sr),
#                          *bandwidth(audio,sr),*melspectrogram(audio,sr),*rms(audio)])
#     m, v = mfcc(audio,sr)
#     for i in range(0, n_mfcc):
#         instance = np.append(instance, [m[i], v[i]])
#     return instance

def run_features_script():
    print("\n*** START ***")
    # Record the start time
    start_time = time.time()
    header = create_data_table_header()
    csvfile, writer = create_data_table_csv("dataset_filter_30_sec.csv")
    writer.writerow(header)          
    for singer in singers:
        singer_dir = "./audios/%s"%singer
        for num in range(0, playlist_size):
            audio_path = "%s/audio-%s.wav"%(singer_dir, num)
            print(audio_path)
            audio_ori, sr, _ = filter.audio_data(audio_path)
            audio_rev = filter.audio_reverse(audio_ori)
            audio_lp, *_ = filter.lowpass_filter(audio_ori, sr)
            audio_bp, *_ = filter.bandpass_filter(audio_ori, sr)
            audio_hp, *_ = filter.highpass_filter(audio_ori, sr)
            instances = [create_instance(singer, num, 'original', audio_ori, sr),
                        create_instance(singer, num, 'reverse', audio_rev, sr),
                        create_instance(singer, num, 'lowpass', audio_lp, sr),
                        create_instance(singer, num, 'bandpass', audio_bp, sr),
                        create_instance(singer, num, 'highpass', audio_hp, sr)]
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
run_features_script()