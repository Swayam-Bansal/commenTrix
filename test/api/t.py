import whisper

audio_file = "/Users/aviralbansal/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/HACKPSU/commenTrix/test/api/audio.wav"
output_file = "transcript.txt"

try:
    model = whisper.load_model("base")
    result = model.transcribe(audio_file)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(result["text"])
    print(f"Transcript saved to {output_file}")
except Exception as e:
    print(f"An error occurred: {e}")