import subprocess
import json
from datetime import datetime

class CommandLineExecutionService:
    def __init__(self):
        pass

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



# if __name__ == "__main__":
#     db_connection_string = "mongodb://localhost:27017/"  # Replace with your MongoDB connection string
#     service = CommandLineExecutionService(db_connection_string)

#     actions = {
#         "actions_before": ["echo 'Starting...'", "ls -l"],
#         "actions_after": ["echo 'Done!'", "cat /etc/passwd"]
#     }

#     actions_json = json.dumps(actions)

#     service.save_actions(actions_json)

#     outputs = service.execute_actions(actions_json)

#     for output in outputs:
#         print(f"Command: {output['command']}, Output: {output['output']}, Type: {output['type']}")
