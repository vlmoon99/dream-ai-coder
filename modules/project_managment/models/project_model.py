from datetime import datetime
from bson import ObjectId


class ProjectModel:
    def __init__(self, name, current_stage,technology, created_at=None, updated_at=None, _id=None):
        self.id = _id if _id else str(ObjectId())
        self.name = name
        self.current_stage = current_stage
        self.technology = technology
        self.created_at = created_at if created_at else datetime.utcnow()
        self.updated_at = updated_at if updated_at else datetime.utcnow()


    def to_dict(self, include_id=True):
        """Convert the ProjectModel to a dictionary format for MongoDB."""
        data = {
            "name": self.name,
            "technology" : self.technology,
            "current_stage": self.current_stage,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at
        }
        if include_id:
            data["_id"] = self.id 
        return data

    @staticmethod
    def from_dict(data):
        """Convert a dictionary format from MongoDB to a ProjectModel object."""
        return ProjectModel(
            _id=data.get("_id", None),
            name=data.get("name", None),
            technology=data.get("technology", None),
            current_stage=data.get("current_stage", None),
            created_at=data.get("createdAt", None), 
            updated_at=data.get("updatedAt", None)
        )
