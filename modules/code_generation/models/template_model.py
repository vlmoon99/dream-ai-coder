from datetime import datetime
from bson import ObjectId

class TemplateModel:
    def __init__(self, author, technology, description, stage, llm_response_template, user_prompt_template, example, standard_of_saving_output,actions, created_at=None, updated_at=None, _id=None):
        self.id = _id if _id else str(ObjectId())
        self.technology = technology 
        self.author = author
        self.stage = stage  
        self.llm_response_template = llm_response_template 
        self.user_prompt_template = user_prompt_template
        self.example = example
        self.description = description
        self.standard_of_saving_output = standard_of_saving_output
        self.actions = actions
        self.created_at = created_at if created_at else datetime.utcnow()
        self.updated_at = updated_at if updated_at else datetime.utcnow()

    def to_dict(self, include_id=True):
        """Convert the TemplateModel to a dictionary format for MongoDB."""
        data = {
            "technology": self.technology,
            "author": self.author,
            "stage": self.stage,
            "llm_response_template": self.llm_response_template,
            "user_prompt_template": self.user_prompt_template,
            "example": self.example,
            "description": self.description,
            "standard_of_saving_output": self.standard_of_saving_output,
            "actions" : self.actions,
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
            llm_response_template=data.get("llm_response_template", None),
            user_prompt_template=data.get("user_prompt_template", None),
            example=data.get("example", None),
            description=data.get("description", None),
            standard_of_saving_output=data.get("standard_of_saving_output", None),
            actions=data.get("actions", None),
            created_at=data.get("createdAt", None),
            updated_at=data.get("updatedAt", None)
        )
