from pymongo.collection import Collection

from chalicelib.database.connection import db

User: Collection = db.get_collection('users')
