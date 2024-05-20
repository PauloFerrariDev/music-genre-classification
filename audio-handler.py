import librosa
import sounddevice as sd
import matplotlib.pyplot as plt
import numpy as np

audio_path = './audios/raimundos/audio-0.wav'
y , sr = librosa.load(audio_path)
duration = y.size / sr
time = np.linspace(0, duration, num=y.size)
print(type(y), type(sr))
print(y.shape, sr, duration)
#sd.play(y, sr)
#sd.wait()
plt.plot(time, y)
plt.show()