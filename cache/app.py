import os
import pymongo
from fastapi import FastAPI


app = FastAPI()
client = pymongo.MongoClient(
    f"mongodb://{os.getenv('MONGO_INITDB_ROOT_USERNAME')}:{os.getenv('MONGO_INITDB_ROOT_PASSWORD')}@mongo:27017")


@app.get("/mvg_avg/")
def get_mvg_avg():
    print("hello")
    cache = client.mvg_avg.cache
    doc = cache.find_one()
    if doc is None:
        # Do API call
        doc = {"fake": "doc"}
        print("Uploading fake doc")
        cache.insert_one(doc)

    del doc["_id"]
    return doc
