#!/usr/bin/env python3
import sys
import os
from venv import create
import dotenv
import glob

from zict import File
# import pdoc

# TODO: Implement container for the code to be executed
# TODO: Implement linting for the code that will be executed (ruff)
# TODO: Implement testing for the code that will be executed
# TODO: Implement a way to run the code in a separate container
# TODO: Implement a way to run the code in a separate container with a specific version of Python
# TODO: Make sure variables are statically typed
# TODO: Implement document generation
# TODO: Implement file structue generation

PYTHON_VERSION = '3.12.0'
PROGRAM_FILE = 'main.py' # TODO: change this to the file that will be executed

def create_folder(folder: str):
    try:
        os.mkdir(f'./{folder}')
    except FileExistsError:
        pass

def init():
    """Create file structure for the project"""
    print(os.getcwd())

    # Create folder structure
    create_folder('docs')
    create_folder('src')
    create_folder('tests')
    
    
    python_files = glob.glob('**/*.py', recursive=True)
    for file in python_files:
        print(file)
        if file.startswith('test_'):
            os.rename(file, f'./tests/{file}')
        else:
            os.rename(file, f'./src/{file}')

    # Create the init files
    with open('./tests/__init__.py', 'a') as f: f.write('')
    with open('./src/__init__.py', 'a') as f: f.write('')

    # Create the env file
    with open('./src/.env', 'a') as f: f.write('')

    # Create the gitignore file
    with open('./.gitignore', 'w') as f: f.write('*.pyc\n__pycache__\n.DS_Store\nenv\n.env\n')

    # Create the Dockerfile
    with open('./Dockerfile', 'w') as f: f.write(f'FROM python:{PYTHON_VERSION}\n\nWORKDIR /src\n\nCOPY ./src .\n\nCMD ["python3", "{PROGRAM_FILE}"]') # TODO: make sure to update this to the correct file
    
    # Create the docker compose file
    with open('./docker-compose.yml', 'w') as f: f.write('version: "3"\nservices:\n  app:\n    build: .\n    volumes:\n      - .:/src\n    command: python3 main.py') # TODO: make sure to update this to the correct file

    # Create the requirements file
    with open('./requirements.txt', 'a') as f: f.write('') # update this as things are being added

    # create README file
    with open('./README.md', 'w') as f: f.write('') # TODO: update this with the project description

    # create license file
    with open('./LICENSE', 'w') as f: f.write('') # TODO: update this with the correct license

    
# TODO: use pipreqs to install modules into requirements.txt

if __name__ == "__main__":
    # if len(sys.argv) < 2:
    #     print("Please provide the path to the Python file as an argument")
    #     sys.exit(1)

    # file_path = sys.argv[1]

    init()
    
    # change this to run within the docker container
    # try:
    #     exec(open(file_path).read())
    # except Exception as e:
    #     print(f"An error occurred while running the file: {e}")
    #     sys.exit(1)