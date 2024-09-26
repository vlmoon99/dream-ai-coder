import os

class FileService:
    def __init__(self):
        pass

    def create_folder(self, path: str) -> None:
        """
        Creates a folder at the specified path.

        Args:
            path (str): The path where the folder should be created.

        Raises:
            OSError: If the folder cannot be created due to permission issues or other OS-level errors.
        """
        try:
            os.makedirs(path, exist_ok=True)  # Creates the folder; no error if it already exists
            print(f"Folder created successfully at: {path}")
        except OSError as e:
            print(f"Error creating folder at {path}: {e}")

    def create_file(self, name: str, content: str, path: str) -> None:
        """
        Creates a file with the given name and content at the specified path.

        Args:
            name (str): The name of the file to create.
            content (str): The content to write inside the file.
            path (str): The directory path where the file should be created.

        Raises:
            OSError: If the file cannot be created due to permission issues or other OS-level errors.
        """
        try:
            self.create_folder(path)
            
            file_path = os.path.join(path, name)
            
            with open(file_path, 'w') as file:
                file.write(str(content))
            print(f"File '{name}' created successfully at: {file_path}")
        except OSError as e:
            print(f"Error creating file '{name}' at {path}: {e}")
