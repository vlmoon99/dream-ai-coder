import requests
import json

class OlamaService:
    
    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url


    def compare_keys(self,template_keys, response_keys):
        """
        Compare the keys from the template and the response.
        """
        return list(template_keys)[:2] == list(response_keys)[:2]


    def extract_keys_from_json(self, json_obj):
        """
        Recursively extract all keys from a nested dictionary structure.
        If 'next_generation_task' is not in the final set of keys, add it.
        """
        keys = set()

        if isinstance(json_obj, dict):
            for key, value in json_obj.items():
                keys.add(key)
                if isinstance(value, dict):
                    keys.update(self.extract_keys_from_json(value))

        if 'next_generation_task' not in keys and 'generated_data' in keys:
            keys.add('next_generation_task')

        return keys

    def generate(self, prompt, llm_response_template):
        """
        Generate data recursively based on a given prompt and template, ensuring that 
        the structure matches the provided template and handling next_generation_task.
        """

        data = {
            "model": "codestral:latest",
            "prompt": prompt,
            "format": "json",
            "stream": False,
            "keep_alive": 30
        }

        generated_data = [] 

        template_keys = self.extract_keys_from_json(json.loads(llm_response_template))
        def recursive_generation(current_prompt):
            data['prompt'] = current_prompt
            try:
                for attempt in range(5):
                    response = requests.post(f"{self.base_url}/api/generate", json=data).json()
                    llm_response = json.loads(response.get("response", "{}"))

                    print(llm_response)
                    response_keys = self.extract_keys_from_json(llm_response)
                    
                    if self.compare_keys(template_keys, response_keys):
                        print(f"Valid response on attempt {attempt + 1}")
                        break
                    else:
                        print(f"Attempt {attempt + 1}: Invalid response structure. Expected keys: {template_keys}, but got: {response_keys}")
                        data['prompt'] =  f"Attempt {attempt + 1}: Invalid response structure. Expected keys: {template_keys}, but got: {response_keys}" + ", Regenerate data using this prompt :" + prompt
                else:
                    raise Exception(f"Failed to generate a valid response after 5 attempts.")


                data_chunk = llm_response.get("generated_data", [])
                if data_chunk:
                    generated_data.extend(data_chunk)
                else:
                    raise Exception("No generated data found in the LLM response.")


                next_generation_task = llm_response.get("next_generation_task", [])
                if next_generation_task:
                    new_prompt = f"{prompt} \n Focus only on generating: {next_generation_task} , didn't repeat generated_data : {generated_data}"
                    recursive_generation(new_prompt)

            except Exception as e:
                print(e.args)
                raise Exception(f"Error generating completion: {str(e)}")


        recursive_generation(prompt)

        if not generated_data:
            raise Exception("Failed to generate any valid data.")

        return generated_data



