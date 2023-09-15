import requests
import os 
from pathlib import Path

# URL of the API endpoint
url = 'https://fastapitraducter.azurewebsites.net/htm_to_json/'


def apiCallObject(path):
    """Call the API endpoint with a file .htm as parameter."""
    with open(path, 'rb') as file:

        #check if it is a file
        if not isFile(path):
            raise ValueError(f"The path {path} is not a file.")

        # Define the files dictionary with the file data
        files = {'file': ('filename.htm', file)}
        # Make the POST request
        response = requests.post(url, files=files)

        return response.text
    
def isDir(path):
    """Check if a path is a directory."""
    if not os.path.exists(path):
        raise ValueError(f"The path {path} does not exist.")
    return os.path.isdir(path)

def isFile(path):
    """Check if a path is a file."""
    if not os.path.exists(path):
        raise ValueError(f"The path {path} does not exist.")
    return os.path.isfile(path)

def extract_dir_name(path):
    """Extract the directory name from a path."""
    if not os.path.exists(path):
        raise ValueError(f"The path {path} does not exist.")
    if not isDir(path):
        raise ValueError(f"The path {path} is not a directory.")
    return os.path.basename(path)

def extract_file_name(path):
    """Extract the file name from a path."""
    if not os.path.exists(path):
        raise ValueError(f"The path {path} does not exist.")
    if not isFile(path):
        raise ValueError(f"The path {path} is not a file.")
    return os.path.basename(path)


def has_json_in_it(path):
    """Check if a directory contains a json file with the same name of the directory."""
    if not isDir(path):
        raise ValueError(f"The path {path} is not a directory.")
    
    dir_name = extract_dir_name(path)
    for element in os.listdir(path):
        if element == dir_name + ".json":
            return True

    return False


def get_htm_file_path_recursive(folder_name: str) -> str:
    """Return the path of 'to_print.htm' inside the specified folder or its subfolders. 
    Raise an error if not found."""
    
    if not isDir(folder_name):
        raise ValueError(f"The path {folder_name} is not a directory.")

    # Convert folder name to a Path object
    folder_path = Path(folder_name)
    
    # Search for the file recursively
    matches = list(folder_path.rglob("toprint.htm"))
    
    # If found, return the first match
    if matches:
        return str(matches[0])
    else:
        raise FileNotFoundError(f"'to_print.htm' not found in {folder_name} or its subfolders")

