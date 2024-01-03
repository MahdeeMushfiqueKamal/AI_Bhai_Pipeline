import pymongo
import os
from constants import atlas_username, atlas_password

client = pymongo.MongoClient(
    f"mongodb+srv://{atlas_username}:{atlas_password}@cluster0.ds5ggbq.mongodb.net/?retryWrites=true&w=majority"
)

def get_db():
    return client.get_database("ai_bhai")