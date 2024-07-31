from gpt4all import GPT4All
from models.business_requirements import BusinessRequirements
import json
import re

class AIGenerationService:
    def __init__(self):
        list_gpus = GPT4All.list_gpus()
        list_gpus = [gpu for gpu in list_gpus if "cuda:" in gpu]
        self.computer_devices = list_gpus
        self.llm_model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf",device=list_gpus[0]) 
        print("Create AIGenerationService")


    def extract_dart_code(self,response : str):
        pattern = r'```\n(.*?)```'
        match = re.search(pattern, response, re.DOTALL)
        if match is None:
                
                pattern = r'```dart\n(.*?)```'
                match = re.search(pattern, response, re.DOTALL)

        if match:
            return match.group(1).strip()
        else:
            return "No code block found."
        
    def parse_generated_entities(self,response: str):
        try:
            # Load the initial JSON response
            # Extract the JSON portion of the string
            start_index = response.find('{')
            end_index = response.rfind('}') + 1
            json_string = response[start_index:end_index]

            response_json = json.loads(json_string)

            return response_json

        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            return []

        

    def generate_text_from_prompt(self,prompt : str):
        with self.llm_model.chat_session():
            response = self.llm_model.generate(prompt, max_tokens=2048)
            return response

    def execute_command(self):
        print("executeCommand")
