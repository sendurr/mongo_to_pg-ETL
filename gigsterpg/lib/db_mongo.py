"""MongoDB connection"""
import os

from pymongo import MongoClient

gigster_db_url = os.environ['DB_URL_MONGO'].strip()
db_name = os.environ['DB_URL_MONGO'].split('/')[-1].strip()
gigster_db = MongoClient(gigster_db_url)[db_name]
