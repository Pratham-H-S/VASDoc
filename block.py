from pymongo import MongoClient

cl = MongoClient("mongodb://192.168.1.1:27017")
db = cl["epochs"]
collections = db["epochs"]
collections.insert_one({"key":"value"})