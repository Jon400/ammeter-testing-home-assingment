import os


class FileUtils:
    @staticmethod
    def read_file(file_path: str) -> str:
        """Read the content of a file and return it as a string."""
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    @staticmethod
    def write_file(file_path: str, content: str):
        """Write the given content to a file."""
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

    @staticmethod
    def append_to_file(file_path: str, content: str):
        """Append the given content to a file."""
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(content)

    @staticmethod
    def file_exists(file_path: str) -> bool:
        """Check if a file exists."""
        return os.path.isfile(file_path)

    @staticmethod
    def delete_file(file_path: str):
        """Delete a file if it exists."""
        if os.path.isfile(file_path):
            os.remove(file_path)

    @staticmethod
    def create_folder(folder_path: str):
        """Create a folder (and its parents) if it does not exist."""
        os.makedirs(folder_path, exist_ok=True)

    @staticmethod
    def list_files(folder_path: str, extension: str = "") -> list[str]:
        """Return the names of the files in a folder, only those ending with the extension when given."""
        return [
            name for name in os.listdir(folder_path)
            if name.endswith(extension) and os.path.isfile(os.path.join(folder_path, name))
        ]
