import os
import pymongo
import requests
import time
from fastapi import FastAPI


app = FastAPI()
client = pymongo.MongoClient(
    f"mongodb://{os.getenv('MONGO_INITDB_ROOT_USERNAME')}:{os.getenv('MONGO_INITDB_ROOT_PASSWORD')}@mongo:27017")


@app.get("/mvg_avg/")
def get_mvg_avg():
    print("hello")

    cache = client.mvg_avg.cache
    docs = cache.find(sort=[("_time", pymongo.DESCENDING)])
    print(docs)

    cache_doc = None
    for doc in docs:
        print(doc)
        if doc is not None:
            if "_time" not in doc:            
                cache.delete_one(doc)
                doc = None
            elif time.time() - doc["_time"] > 1:
                cache.delete_one(doc)
                doc = None
            else:
                cache_doc = doc
                cache.delete_many(filter={})
            

    if cache_doc is None:
        # Do API call
        try:
            price = requests.get(
                "http://api:8000/mvg_avg/")

        except Exception as e:
            print(f"Error: {e}")
            return {"price": 0}

        cache_doc = price.json()        
        cache_doc['_time'] = time.time()

    cache.insert_one(cache_doc)

    del cache_doc["_id"]
    return cache_doc
