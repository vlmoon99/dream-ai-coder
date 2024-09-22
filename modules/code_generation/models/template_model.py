from datetime import datetime
from bson import ObjectId


class TemplateModel:
    def __init__(self, author, technology, description, stage, template, example, created_at=None, updated_at=None, _id=None):
        self.id = _id if _id else str(ObjectId())
        self.technology = technology 
        self.author = author
        self.stage = stage  
        self.template = template 
        self.example = example
        self.description = description
        self.created_at = created_at if created_at else datetime.utcnow()
        self.updated_at = updated_at if updated_at else datetime.utcnow()

    def to_dict(self, include_id=True):
        """Convert the TemplateModel to a dictionary format for MongoDB."""
        data = {
            "technology": self.technology,
            "author": self.author,
            "stage": self.stage,
            "template": self.template,
            "example": self.example,
            "description": self.description,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at
        }
        if include_id:
            data["_id"] = self.id
        return data

    @staticmethod
    def from_dict(data):
        """Convert a dictionary format from MongoDB to a TemplateModel object."""
        return TemplateModel(
            _id=data.get("_id", None),
            technology=data.get("technology", None),
            author=data.get("author", None),
            stage=data.get("stage", None),
            template=data.get("template", None),
            example=data.get("example", None),
            description=data.get("description", None),
            created_at=data.get("createdAt", None),
            updated_at=data.get("updatedAt", None)
        )
