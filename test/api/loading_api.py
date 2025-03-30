from dotenv import load_dotenv, find_dotenv
import os

env_path = find_dotenv()
print("Using .env from:", env_path)

load_dotenv(env_path, override=True)
print("YOUTUBE_API_KEY:", os.getenv("YOUTUBE_API_KEY"))
