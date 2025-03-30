import yt_dlp
import os

def download_youtube_audio(youtube_url, output_filename="test/audio.wav"):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_filename,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])
    return output_filename

youtube_url = "https://www.youtube.com/watch?v=s4pYfSqAOtE"
audio_file = download_youtube_audio(youtube_url)
print(f"Audio downloaded to: {audio_file}")

#remember to delete the audio file after whisper is finished.