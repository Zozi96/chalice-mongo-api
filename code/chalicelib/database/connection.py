from decouple import config
from pymongo import MongoClient

MONGO_HOST = config('MONGO_HOST', default='localhost', cast=str)
MONGO_USERNAME = config('MONGO_USERNAME', default='myuser', cast=str)
MONGO_PASSWORD = config('MONGO_PASSWORD', default='mypassword', cast=str)
MONGO_DBNAME = config('MONGO_DBNAME', default='mydb', cast=str)

client = MongoClient(f'mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}/?retryWrites=true&w=majority')
db = client.get_database(MONGO_DBNAME)


