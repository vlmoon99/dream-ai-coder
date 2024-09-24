import requests

class OlamaService:
    
    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url

    def generate(self, prompt, template, example):
        
        prompt = (
            f"This is the template by which you will generate code ---> : {template} "
            f"This is the example of how to write response ---> : {example} "
            f"This is the requirements of the response ---> : It must contains list of entity in json format as liek this one : [first_entity,second_entity, ...] ,"
            f"If there will be a lot of data to generate you can add which entity you want to generate in new map entry with key -> continue_to_generate with value as list with entity name as user,post,task, etcs [user,post,task] ,"
            f"This is prompt ---> : {prompt}"
        )
        
        data = {
            "model": "codestral:latest",
            "prompt": prompt,
            "format": "json",
            "stream": False,
            "keep_alive": 30
        }

        response = requests.post(f"{self.base_url}/api/generate", json=data)
        return response.json()



