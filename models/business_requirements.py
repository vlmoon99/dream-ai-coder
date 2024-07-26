from models.user_requirements import UserRequirements

class BusinessRequirements:
    def __init__(self, user_requirements: UserRequirements):
        self.requirements = self._transform_requirements(user_requirements)

    def _transform_requirements(self, user_requirements: UserRequirements) -> str:
        # Here we can transform user input into structured business requirements.
        # For simplicity, let's assume a simple transformation.
        return user_requirements.description.upper()

    def update_requirements(self, new_description: str):
        self.requirements = self._transform_requirements(UserRequirements(new_description))

    def __repr__(self):
        return f"BusinessRequirements(requirements={self.requirements})"
