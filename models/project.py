from models.template import Template
from models.business_requirements import BusinessRequirements

class Project:
    def __init__(self, name: str, path: str, template: Template, business_requirements : BusinessRequirements):
        self.name = name
        self.path = path
        self.template = template
        self.business_requirements = business_requirements

    def proceed_to_next_stage(self):
        current_stage = self.template.get_next_stage()
        if current_stage:
            current_stage.complete_stage()
            return f"Proceeding to the next stage: {current_stage.name}"
        else:
            return "All stages are completed."

    def __repr__(self):
        return (
            f"Project(name={self.name}, path={self.path}, template={self.template.name}, "
            f"user_requirements={self.user_requirements}, business_requirements={self.business_requirements})"
        )
