from pytube import Playlist, YouTube
from io import BytesIO
import ffmpeg
import filter
import os

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
playlists = [
  "https://youtube.com/playlist?list=PLAjEgfN1lYafJXIZco9RFCfSegyo7knOt", # elza-soares
  "https://youtube.com/playlist?list=PLxFfose56AjeNyJjGhbguYhPBCTZks9Lc", # rita-lee
  "https://youtube.com/playlist?list=PLfTHnLd-UmHMyjNSxYn7vPDEC7hbAXE4g", # roberta-miranda
  "https://youtube.com/playlist?list=PLE6CB1BD95D51A8CA",                 # roberta-sa
  "https://youtube.com/playlist?list=PLPhmvZL4T7BB2V0NiuqNUCLDFpqXOPt9D", # cassia-eller
  "https://youtube.com/playlist?list=PL1EFB0F9942717155",                 # racionais-mcs
  "https://youtube.com/playlist?list=PLPhmvZL4T7BBcR8YXX-DwCoQMdEMKVTbt", # raimundos
  "https://youtube.com/playlist?list=PL2652111017CAD76C",                 # planet-hemp
  "https://youtube.com/playlist?list=PL_lW1_PMwv7O3faHITOGujtZx89Xj1Rhb", # natiruts
  "https://youtube.com/playlist?list=PL5OidG0sGjBoH1NkRBhO9J2T8Jyj471Lr", # jorge-ben-jor
]
playlist_size = 30

#* Buffering audio stream using Pytube
def audio_buffer(url:str):
    yt = YouTube(url)
    stream = yt.streams.get_audio_only()
    print("TITLE:", stream.title, "FILESIZE:", stream.filesize, "TYPE:", stream.type, "SUBTYPE:", stream.subtype)
    buffer = BytesIO()
    stream.stream_to_buffer(buffer)
    return buffer

#* Process audio buffer using ffmpeg
def process(buffer:BytesIO, output_file:str, ss="01:30"):
    process = (
            ffmpeg
            .input('pipe:', ss=ss, t="30", ac=2, format="mp4")
            .output(output_file, ac=1, format="wav")
            .overwrite_output()
            .run_async(pipe_stdin=True)
        )
    try:
        process.communicate(input=buffer.getbuffer(), timeout=None)
        process.wait() # Wait for ffmpeg process to finish
    except Exception as e:
        print("Error:", e)

#* Create directory for singer's audios
def create_directory(dir:str):
    if not os.path.exists(dir): # checking if the directory exist or not     
        os.makedirs(dir) # if the directory is not present then create it

#* Iterate over playlists array
def playlists_handler():
    for(singer, playlist) in zip(singers, playlists):
        singer_dir = "./audios/%s"%singer
        create_directory(singer_dir)
        pl = Playlist(playlist)[:playlist_size]
        for i in range(0, playlist_size):
            url = pl[i]
            output_file = "%s/audio-%s.wav"%(singer_dir, i)
            process(audio_buffer(url), output_file)
            
def audios_below_30sec():
    for singer in singers:
        singer_dir = "./audios/%s"%singer
        for i in range(0, playlist_size):
            audio_path = "%s/audio-%s.wav"%(singer_dir, i)
            audio, sr, _ = filter.audio_data(audio_path)
            duration = audio.size/sr
            if(duration<30):
                print(audio_path)

def fix_audios():
    process(buffer=audio_buffer("https://www.youtube.com/watch?v=_emCHu4ECS0&list=PLPhmvZL4T7BBcR8YXX-DwCoQMdEMKVTbt&index=18"),output_file="./audios/raimundos/audio-17.wav", ss="00:10")
    process(buffer=audio_buffer("https://www.youtube.com/watch?v=_zld8rkIhZk&list=PLAjEgfN1lYafJXIZco9RFCfSegyo7knOt&index=13"),output_file='./audios/elza-soares/audio-12.wav', ss="00:10")
    process(buffer=audio_buffer("https://www.youtube.com/watch?v=QuDYmfUEakA&list=PL1EFB0F9942717155&index=23"),output_file='./audios/racionais-mcs/audio-22.wav', ss="00:10")
    process(buffer=audio_buffer("https://www.youtube.com/watch?v=kU2tZZQpENA&list=PLPhmvZL4T7BBcR8YXX-DwCoQMdEMKVTbt&index=24"),output_file='./audios/raimundos/audio-23.wav', ss="00:10")
    process(buffer=audio_buffer("https://www.youtube.com/watch?v=SctRTbfJfBE&list=PL2652111017CAD76C&index=17"),output_file='./audios/planet-hemp/audio-16.wav', ss="00:10")
    process(buffer=audio_buffer("https://www.youtube.com/watch?v=N7mJ6-_zm08&list=PL2652111017CAD76C&index=24"),output_file='./audios/planet-hemp/audio-23.wav', ss="00:25")
    process(buffer=audio_buffer("https://www.youtube.com/watch?v=zDYDqbmKpXg&list=PL2652111017CAD76C&index=33"),output_file='./audios/planet-hemp/audio-28.wav', ss="00:30")
    process(buffer=audio_buffer("https://www.youtube.com/watch?v=OjWET9ZCWus&list=PL5OidG0sGjBoH1NkRBhO9J2T8Jyj471Lr&index=30"),output_file='./audios/jorge-ben-jor/audio-29.wav', ss="00:05")

#* Main function
def run_download_script():
    print("\n*** START ***")
    audios_below_30sec()  
    # fix_audios()
    print("*** END ***\n")

#* Run script
# run_download_script()