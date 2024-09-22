from pymongo import MongoClient
from bson import ObjectId
from ..models.technology_model import TechnologyModel
from datetime import datetime
from pymongo.server_api import ServerApi


class TechnologyRepository:
    def __init__(self, uri="mongodb+srv://vlmoon:dreamaicoder@cluster0.izbgd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0", db_name="app_project"):
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = self.client[db_name]
        self.collection = self.db["technologies"]
        try:
            self.client.admin.command('ping')
            print("Successfully connected to MongoDB!")
        except Exception as e:
            print(e)

    def create(self, technology: TechnologyModel):
        """Insert a new Technology into the database."""
        self.collection.insert_one(technology.to_dict())
        return technology

    def get_by_id(self, technology_id):
        """Retrieve a Technology by its ID."""
        data = self.collection.find_one({"_id": technology_id})
        return TechnologyModel.from_dict(data) if data else None

    def get_by_technology(self, technology):
        """Retrieve a Technology by its name."""
        data = self.collection.find_one({"technology": technology})
        return TechnologyModel.from_dict(data) if data else None

    def update(self, technology_id, updated_technology: TechnologyModel):
        """Update an existing Technology by its ID."""
        updated_technology.updated_at = datetime.utcnow()
        result = self.collection.update_one(
            {"_id": technology_id},
            {"$set": updated_technology.to_dict(include_id=False)}
        )
        return result.modified_count > 0

    def delete(self, technology_id):
        """Delete a Technology by its ID."""
        result = self.collection.delete_one({"_id": technology_id})
        return result.deleted_count > 0
