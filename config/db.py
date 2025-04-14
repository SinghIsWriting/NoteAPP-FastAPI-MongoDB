from pymongo import MongoClient
from decouple import AutoConfig

# Load environment variables
config = AutoConfig(search_path=".")

MONGODB_URI = config("MONGODB_URI", default="mongodb://localhost:27017/")

conn = MongoClient(MONGODB_URI)
