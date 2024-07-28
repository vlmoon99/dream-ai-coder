from gpt4all import GPT4All
from models.business_requirements import BusinessRequirements

class AIGenerationService:
    def __init__(self):
        list_gpus = GPT4All.list_gpus()
        list_gpus = [gpu for gpu in list_gpus if "cuda:" in gpu]
        self.computer_devices = list_gpus
        self.llm_model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf",device=list_gpus[0]) 
        print("Create AIGenerationService")

    def generateCode(self,prompt : str):
        with self.llm_model.chat_session():
            generarted_content = self.llm_model.generate(prompt, max_tokens=2048)
            return generarted_content

    def executeCommand(self):
        print("executeCommand")
