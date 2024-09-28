from pymongo import MongoClient
from bson import ObjectId
from ..models.template_model import TemplateModel
from datetime import datetime
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()


class TemplateRepository:
    def __init__(self, db_name="app_project"):
        
        mongodb_user = os.getenv("MONGODB_USER")
        mongodb_pass = os.getenv("MONGODB_PASS")
        mongodb_url = os.getenv("MONGODB_URL")
        
        uri = f"mongodb+srv://{mongodb_user}:{mongodb_pass}@{mongodb_url}/?retryWrites=true&w=majority&appName=Cluster0"

        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = self.client[db_name]
        self.collection = self.db["templates"]
        try:
            self.client.admin.command('ping')
        except Exception as e:
            print(e)

    def create(self, template: TemplateModel):
        """Insert a new Template into the database."""
        self.collection.insert_one(template.to_dict())
        return template

    def get_by_id(self, template_id):
        """Retrieve a Template by its ID."""
        data = self.collection.find_one({"_id": template_id})
        return TemplateModel.from_dict(data) if data else None

    def get_template_by_tech_and_author(self, technology,author,stage):
        """Retrieve a Template by its ID."""
        data = self.collection.find_one(
            {"author": author, "technology": technology, "stage": stage})
        return TemplateModel.from_dict(data) if data else None


    def update(self, template_id, updated_template: TemplateModel):
        """Update an existing Template by its ID."""
        updated_template.updated_at = datetime.utcnow()
        result = self.collection.update_one(
            {"_id": template_id},
            {"$set": updated_template.to_dict(include_id=False)}
        )
        return result.modified_count > 0

    def delete(self, template_id):
        """Delete a Template by its ID."""
        result = self.collection.delete_one({"_id": template_id})
        return result.deleted_count > 0
