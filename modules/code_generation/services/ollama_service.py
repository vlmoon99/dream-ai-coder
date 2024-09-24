import requests

class OlamaService:
    
    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url

    def generate(self, prompt, template, example):
        
        prompt = (
            f"This is the example of how to write response ---> : {example} "
            f"This is the template by which you will generate code ---> : {template} "
            f"This is prompt ---> : {prompt}"
        )
        
        print(f"My prompt is : {prompt}")

        data = {
            "model": "codellama",
            "prompt": prompt,
            "format": "json",
            "stream": False,
            "keep_alive": 30
        }

        response = requests.post(f"{self.base_url}/api/generate", json=data)
        return response.json()



