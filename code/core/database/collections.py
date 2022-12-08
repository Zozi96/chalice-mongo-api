from pymongo.collection import Collection

from core.database.connection import db

User: Collection = db.get_collection('users')
