from datetime import datetime
from bson import ObjectId


class TechnologyModel:
    def __init__(self, technology, stages, created_at=None, updated_at=None, _id=None):
        self.id = _id if _id else str(ObjectId())
        self.technology = technology
        self.stages = stages
        self.created_at = created_at if created_at else datetime.utcnow()
        self.updated_at = updated_at if updated_at else datetime.utcnow()

    def to_dict(self, include_id=True):
        """Convert the TechnologyModel to a dictionary format for MongoDB."""
        data = {
            "technology": self.technology,
            "stages": self.stages,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at
        }
        if include_id:
            data["_id"] = self.id
        return data

    @staticmethod
    def from_dict(data):
        """Convert a dictionary format from MongoDB to a TechnologyModel object."""
        return TechnologyModel(
            _id=data.get("_id", None),
            technology=data.get("technology", None),
            stages=data.get("stages", 0),
            created_at=data.get("createdAt", None),
            updated_at=data.get("updatedAt", None)
        )
