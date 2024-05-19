from pytube import Playlist, YouTube
import subprocess
from io import BytesIO


singer = [
  "timbalada",
  "camisa-de-venus",
  "ze-ramalho",
  "racionais-mcs",
  "os-mutantes",
  "engenheiros-do-havai",
  "massacration",
  "planet-hemp",
  "biquini-cavadao",
  "nacao-zumbi",
]
playlists = [
  "https://youtube.com/playlist?list=PLgw1BGbJKMAYI3bFNUbLbyTvPihob63zH",
  "https://youtube.com/playlist?list=PLtFyEmGSQH7IrbUeeSurNnK8P22HeBxnO",
  "https://youtube.com/playlist?list=PL8X3mfgw31ZSGBOYe-6KBhb2mWhHxYzJc",
  "https://youtube.com/playlist?list=PL1EFB0F9942717155",
  "https://youtube.com/playlist?list=PLxphGrNq1IDvU46HqcMYsDY34gcpiv7aD",
  "https://youtube.com/playlist?list=PLIyf0d2pGrPPbxzZ6RcmO9ZHhYL0DCtA6",
  "https://youtube.com/playlist?list=PLsgDGqCmHhTQJkjYKsV4PM5bpvQvSNlNp",
  "https://youtube.com/playlist?list=PL2652111017CAD76C",
  "https://youtube.com/playlist?list=PLTRU2u_bXJopcP46wUWjnpJnBKepkDWPn",
  "https://youtube.com/playlist?list=PLZrJ_FXC5XM3p-mVaya7nCydek_qmNEud",
]
# print("\nPlaylists:", playlists, "\n")

# Step 1: Download video stream using Pytube
def download_video(url):
    yt = YouTube(url)
    stream = yt.streams.get_audio_only()
    print("TITLE:", stream.title)
    print("FILESIZE:", stream.filesize)
    print("CODECS:", stream.audio_codec)
    print("TYPE:", stream.type)
    print("SUBTYPE:", stream.subtype)
    filename = "test.%s"%stream.subtype
    stream.download("./audios",filename=filename)
    # return stream
    # saving to buffer
    # buffer = BytesIO()
    # stream.stream_to_buffer(buffer)
    # print(buffer)
    # print(len(buffer))
    return filename

# Step 2: Process video stream using ffmpeg
def process_video(input_file, output_file):
    ffmpeg_cmd = [
        'ffmpeg',
        '-ss', '01:00', '-t', '30',
        '-i', 
         input_file,    
        '-ac', '1', 
        '-f', 'wav',     # Output format
        output_file      # Output file path
    ]
    
    # Run ffmpeg process with input from Pytube stream
    # ffmpeg_process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)
    ffmpeg_process = subprocess.Popen(ffmpeg_cmd)

    # Pipe Pytube stream to ffmpeg process
    # chunk_size = 1024*1024
    # while True:
    #     chunk = stream.on_progress(chunk_size)
    #     if not chunk:
    #         break
    #     ffmpeg_process.stdin.write(chunk)
        
    # Close the stdin pipe to signal the end of input
    # ffmpeg_process.stdin.close()

    # Wait for ffmpeg process to finish
    try:
        ffmpeg_process.wait()
    except Exception as e:
        print("Error:", e)

# Example usage
if __name__ == "__main__":
    print()
    print("START...")

    # video_url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'  # Example YouTube video URL


    p = Playlist(playlists[0])
    a=p[:30]
    url = p[0]
    filename = download_video(url)
    input_file = './audios/%s'%filename    
    output_file = './audios/out.wav'  # Output file path
    print(input_file)
    print(output_file)
    # stream = download_video(url)
    if filename:
        process_video(input_file, output_file)
        print("Video processing complete.")
    else:
        print("Failed to download video stream.")
    print("END\n")


# 'ffmpeg -i ./test.mp4 -c:a copy -preset fast -ss 01:00 -t 30 out.wav'(NOT WORK)
# 'ffmpeg -ss 01:30 -t 30 -i test.mp4 -c copy -map 0:a out.wav' (NOT WORK)
# 'ffmpeg -ss 01:30 -t 30 -i test.mp4 -ac 1 -f wav out.wav'