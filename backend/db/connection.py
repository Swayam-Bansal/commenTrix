import os
import pymongo
from dotenv import load_dotenv

load_dotenv()  # loads .env in the root folder

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = pymongo.MongoClient(MONGO_URI)

db = client["commenTrixDB"]  # name your DB
comments_col = db["comments"]  # collection for storing comments
