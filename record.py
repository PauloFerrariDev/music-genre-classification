import sounddevice as sd
import soundfile as sf
import threading

import os
import shutil

duration=30
samplerate=16000
audio_path = './audios/raimundos/audio-0.wav'
dest_path = 'xxx'
#audio_path = './audios/cassia-eller/audio-0.wav'


def play_audio():
    print("Start Playing.")
    audio, sr = sf.read(audio_path)
    sd.play(audio, samplerate=sr)
    sd.wait()

def record_audio():
    print("Start Recording.")
    audio_rec = sd.rec(int(duration * samplerate), samplerate, channels=1, dtype='float32')
    sd.wait()
    #sf.write('cassia-eller-audio_0.wav', audio_rec, samplerate)
    sf.write(dest_path, audio_rec, samplerate)

def tocar_gravar():
    # Create and start the threads for playback and recording
    play_thread = threading.Thread(target=play_audio)
    record_thread = threading.Thread(target=record_audio)

    play_thread.start()
    record_thread.start()

    # Wait for both threads to finish
    play_thread.join()
    record_thread.join()
    print("Playback and recording finished.")


# Diretório de origem e destino
directorio_principal = './audios'
directorio_destino = './audios_gravados'

if not os.path.exists(directorio_destino):
    os.makedirs(directorio_destino)

# Lista todos os itens no diretório de origem
for item in os.listdir(directorio_principal):
    pasta_banda = os.path.join(directorio_principal, item)
    pasta_nova = os.path.join(directorio_destino, item)
    if not os.path.exists(pasta_nova):
        os.makedirs(pasta_nova)

    # Se o item é uma pasta, copia para o destino
    if os.path.isdir(pasta_banda):
        for item2 in os.listdir(pasta_banda):
            audio_path = pasta_banda + '\\' + item2
            dest_path = pasta_nova + '\\and-' + item2
            tocar_gravar()
