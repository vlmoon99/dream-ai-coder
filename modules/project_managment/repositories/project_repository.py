from pymongo import MongoClient
from bson import ObjectId
from ..models.project_model import ProjectModel
from datetime import datetime
from pymongo.server_api import ServerApi


class ProjectRepository:
    def __init__(self, uri="mongodb+srv://vlmoon:dreamaicoder@cluster0.izbgd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0", db_name="app_project"):
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = self.client[db_name]
        self.collection = self.db["projects"]
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)


    def create(self, project: ProjectModel):
        """Insert a new Project into the database."""
        self.collection.insert_one(project.to_dict())
        return project

    def get_by_id(self, project_id):
        """Retrieve a Project by its ID."""
        data = self.collection.find_one({"_id": project_id})
        return ProjectModel.from_dict(data) if data else None


    def update(self, project_id, updated_project: ProjectModel):
        """Update an existing Project by its ID."""
        updated_project.updated_at = datetime.utcnow()
        result = self.collection.update_one(
            {"_id": project_id},  
            {"$set": updated_project.to_dict(include_id=False)}
        )
        return result.modified_count > 0


    def delete(self, project_id):
        """Delete a Project by its ID."""
        result = self.collection.delete_one({"_id": project_id})
        return result.deleted_count > 0
