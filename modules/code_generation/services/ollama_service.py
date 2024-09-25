import requests
import json

class OlamaService:
    
    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url

    def generate(self, prompt):
        
        data = {
            "model": "codestral:latest",
            "prompt": prompt,
            "format": "json",
            "stream": False,
            "keep_alive": 30
        }

        response = requests.post(f"{self.base_url}/api/generate", json=data)

        return json.loads(response.json().get("response", ""))



