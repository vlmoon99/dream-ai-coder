import subprocess
import json
from datetime import datetime

class CommandLineExecutionService:
    def __init__(self):
        pass

    def format_action(self,action, params):
        try:
            return action.format(**params)
        except KeyError as e:
            print(f"Warning: Missing parameter {e} in action: {action}")
            return action
        except ValueError as e:
            print(f"Warning: Invalid format in action: {action}")
            return action

    def execute_command(self, command):
        """Executes a shell command and returns the output."""
        try:
            result = subprocess.run(command, capture_output=True, text=True, shell=True)
            if result.returncode != 0:
                output = f"Error: {result.stderr.strip()}"
            else:
                output = result.stdout.strip()
                
            if len(output) > 300:
                output = output[-300:]

            return output

        except Exception as e:
            return f"Exception occurred: {str(e)}"