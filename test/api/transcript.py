import whisper
import os

print(os.getcwd())

def transcribe_audio_to_file(audio_file_path, output_file_path):
    """
    Transcribes an audio file using Whisper and saves the transcript to a file.

    Args:
        audio_file_path (str): The path to the audio file.
        output_file_path (str): The path to the output text file.
    """
    try:
        model = whisper.load_model("base")  # You can change to "medium" or "large" for better accuracy
        result = model.transcribe(audio_file_path)
        transcript = result["text"]

        with open(output_file_path, "w", encoding="utf-8") as f:
            f.write(transcript)

        print(f"Transcript saved to {output_file_path}")

    except FileNotFoundError:
        print(f"Error: Audio file not found at {audio_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

audio_file = "test/api/audio.wav"
output_file = "test/api/transcript.txt" #where you want the transcript saved.
transcribe_audio_to_file(audio_file, output_file)