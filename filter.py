import numpy as np
from scipy.signal import butter, lfilter, freqz, spectrogram
import matplotlib.pyplot as plt
import librosa
import sounddevice as sd

two_pi = 2*np.pi
order = 8 # max order for bandpass Butterworth filter without error
Wn = np.array([90, 265])*two_pi # cutoff frequencies [rad/s]
audio_path = './audios/cassia-eller/audio-0.wav'

def audio_data(audio_path: str):
    audio , sr = librosa.load(audio_path) # sr = sampling rate [sample/s]
    duration = audio.size / sr
    t = np.linspace(0, duration, num=audio.size) # samples
    return audio, sr, t

def bandpass_filter(audio, sr):    
    b, a = butter(N=order, Wn=Wn, btype='bandpass', analog=False, output='ba', fs=sr)
    y = lfilter(b, a, audio)
    return y, b, a

def plot_filtered_audio(audio, filtered_audio, sr, b, a, t):
    #* Plot the frequency response.
    w, h = freqz(b, a, fs=sr, worN=8000)
    plt.figure()
    plt.subplot(3, 1, 1)
    plt.plot(w/two_pi, np.abs(h), 'b')
    plt.plot(Wn[0]/two_pi, np.sqrt(2)/2, 'ko')
    plt.axvline(Wn[0]/two_pi, color='r')
    plt.plot(Wn[1]/two_pi, np.sqrt(2)/2, 'ko')
    plt.axvline(Wn[1]/two_pi, color='r')
    plt.xlim(0, 500)
    plt.title("Bandpass Filter Frequency Response")
    plt.xlabel('Frequency [Hz]')
    #* Filter the data, and plot both the original and filtered signals.
    plt.subplot(3, 1, 2)
    plt.plot(t, audio, 'b-')
    plt.title('Audio')
    plt.xlabel('Time [sec]')
    plt.subplot(3, 1, 3)
    plt.plot(t, filtered_audio, 'g-')
    plt.title('Filtered Audio')
    plt.xlabel('Time [sec]')
    plt.subplots_adjust(hspace=0.9)
    #* Spectrogram
    f1, _, sxx1 = spectrogram(audio, sr)
    f2, _, sxx2 = spectrogram(filtered_audio, sr)
    plt.figure()
    plt.subplot(2, 1, 1)
    plt.plot(f1/two_pi, sxx1, 'b-')
    plt.title("Spectrogram (audio)")
    plt.xlabel('Frequency [Hz]')
    plt.xlim(0, 500)
    plt.subplot(2, 1, 2)
    plt.plot(f2/two_pi, sxx2, 'g-')
    plt.title("Spectrogram (filtered audio)")
    plt.xlabel('Frequency [Hz]')
    plt.xlim(0, 500)
    plt.subplots_adjust(hspace=0.6)
    plt.show()

def play_audio(audio, sr):
    sd.play(audio, sr)
    sd.wait()

def play_filtered_audio(filtered_audio, sr):
    sd.play(filtered_audio, sr)
    sd.wait()

#* Main function
def run_filter_script():
    print("\n*** START ***")
    #* Get audio data
    audio, sr, t = audio_data(audio_path)
    #* Filter the audio
    filtered_audio, b, a = bandpass_filter(audio, sr)
    #* Plot filtered audio and its frequency response
    plot_filtered_audio(audio, filtered_audio, sr, b, a, t)
    #* Play audio and audio filtered
    play_audio(audio, sr)
    play_filtered_audio(filtered_audio, sr)
    print("*** END ***\n")

#* Run script
# run_filter_script()