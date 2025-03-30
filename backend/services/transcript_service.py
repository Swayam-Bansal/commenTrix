# backend/services/transcript_service.py
import os
import subprocess
import nltk
import whisper

TRANSCRIPT_STORAGE_PATH = "temp_transcripts" # Or decide on a better storage mechanism

if not os.path.exists(TRANSCRIPT_STORAGE_PATH):
    os.makedirs(TRANSCRIPT_STORAGE_PATH)

def download_youtube_audio(video_url: str, output_path: str):
    """Downloads the audio from a YouTube video."""
    try:
        command = [
            "yt-dlp",
            "-x",  # Extract audio
            "--audio-format",
            "mp3",  # Or another suitable format
            "-o",
            f"{output_path}/%(id)s.%(ext)s",
            video_url,
        ]
        subprocess.run(command, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error downloading audio: {e}")
        return False

def generate_transcript_whisper(audio_file_path: str):
    """Generates a transcript from an audio file using Whisper."""
    try:
        model = whisper.load_model("base") # You can choose different model sizes
        result = model.transcribe(audio_file_path)
        return result["text"]
    except Exception as e:
        print(f"Error generating transcript with Whisper: {e}")
        return None

def get_video_transcript(video_id: str, video_url: str):
    """Downloads audio and generates transcript for a given video ID and URL."""
    audio_output_path = TRANSCRIPT_STORAGE_PATH
    audio_file_name = f"{video_id}.mp3"
    audio_file_path = os.path.join(audio_output_path, audio_file_name)

    if not os.path.exists(audio_file_path):
        print(f"Downloading audio for video ID: {video_id}...")
        if not download_youtube_audio(video_url, audio_output_path):
            return None
        print("Audio download complete.")

    print(f"Generating transcript for video ID: {video_id}...")
    transcript = generate_transcript_whisper(audio_file_path)

    if transcript:
        print("Transcript generation complete.")
        return transcript
    else:
        return None

def segment_transcript(transcript: str):
    """Segments the transcript into sentences."""
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        print("Downloading NLTK 'punkt' data...")
        nltk.download('punkt')
    return nltk.sent_tokenize(transcript)

#This is an example usage; to test each segment sperately, you can call them in isolation.
if __name__ == "__main__":
    # Example usage
    video_url = "https://www.youtube.com/watch?v=s4pYfSqAOtE&ab_channel=LinusTechTips" 
    video_id = "s4pYfSqAOtE"
    transcript_text = get_video_transcript(video_id, video_url)
    if transcript_text:
        print("\n--- Raw Transcript ---")
        print(transcript_text)
        segments = segment_transcript(transcript_text)
        print("\n--- Transcript Segments ---")
        for i, segment in enumerate(segments):
            print(f"{i+1}: {segment}")