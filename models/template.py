from models.environment import Environment

class TemplateStage:
    def __init__(self, name: str, description: str, system_prompt: str = None, prompt_template: str = None):
        self.name = name
        self.description = description
        self.completed = False
        self.system_prompt = system_prompt
        self.prompt_template = prompt_template

    def complete_stage(self):
        self.completed = True

    def __repr__(self):
        return f"TemplateStage(name={self.name}, completed={self.completed})"


class Template:
    def __init__(self, name: str, environment: Environment, stages: list[TemplateStage]):
        self.name = name
        self.environment = environment
        self.stages = stages

    def get_next_stage(self):
        for stage in self.stages:
            if not stage.completed:
                return stage
        return None

    def __repr__(self):
        return f"Template(name={self.name}, environment={self.environment}, stages={self.stages})"
