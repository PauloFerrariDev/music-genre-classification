import numpy as np
from librosa import feature
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

def tempo(audio, sr):
    return feature.tempo(y=audio, sr=sr)[0]

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

def create_data_table_header():
    header = ['singer','filename','tempo','stft_mean','stft_var','cqt_mean','cqt_var','cens_mean','cens_var','contrast_mean','contrast_var','centroid_mean','centroid_var','bandwidth_mean','bandwidth_var','melspectrogram_mean','melspectrogram_var','rms_mean','rms_var']
    for i in range(1, n_mfcc+1):
        header = np.append(header, ['mfcc%s_mean'%i, 'mfcc%s_var'%i])
    return header

def create_instance(singer, num_audio, audio, sr, ):
    filename = "%s/audio-%s.wav"%(singer, num_audio)
    instance = np.array([singer,filename,tempo(audio,sr),*stft(audio,sr),*cqt(audio,sr),
                         *cens(audio,sr),*contrast(audio,sr),*centroid(audio,sr),
                         *bandwidth(audio,sr),*melspectrogram(audio,sr),*rms(audio)])
    m, v = mfcc(audio,sr)
    for i in range(0, n_mfcc):
        instance = np.append(instance, [m[i], v[i]])
    return instance

def run_features_script():
    print("\n*** START ***")
    header = create_data_table_header()
    csvfile, writer = create_data_table_csv("dataset_filter_30_sec.csv")
    writer.writerow(header)          
    for singer in singers:
        singer_dir = "./audios/%s"%singer
        for num in range(0, playlist_size):
            audio_path = "%s/audio-%s.wav"%(singer_dir, num)
            print(audio_path)
            audio, sr, _ = filter.audio_data(audio_path)
            filtered_audio, *_ = filter.bandpass_filter(audio, sr)
            instance = create_instance(singer, num, filtered_audio, sr)
            writer.writerow(instance)
    csvfile.close()
    print("*** END ***\n")
            
#* Run script
run_features_script()