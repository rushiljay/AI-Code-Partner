#!/usr/bin/env python3
import sys
import os
from venv import create
import dotenv
import glob
from pydantic import FilePath
from zict import File
import os
import re
from termcolor import colored
# import pdoc


# TODO: Make note of this projects' dependency

# TODO: Implement container for the code to be executed
# TODO: Implement linting for the code that will be executed (ruff)
# TODO: Implement testing for the code that will be executed
# TODO: Implement a way to run the code in a separate container
# TODO: Implement a way to run the code in a separate container with a specific version of Python
# TODO: Make sure variables are statically typed
# TODO: Implement document generation
# TODO: Implement file structue generation
# TODO: implement file creation
# TODO: stop the running of other functions if not init and setup

PYTHON_VERSION = "3.12.0"
DEFAULT_PROGRAM_FILE = "main.py"  # TODO: change this to the file that will be executed

# TODO: Use this function
def create_file(filePath: str, mode: str = "w", content: str = ""):
    with open(filePath, mode) as f:
        f.write(content)

def create_folder(folder: str):
    try:
        os.mkdir(f"./{folder}")
    except FileExistsError:
        pass

def find_todos_in_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
            file_name = os.path.basename(file_path)
            todos = [(i, line) for (i, line) in enumerate(lines) if "TODO" in line]
            print(
                colored(
                    "\033[1m".join(f"{file_name}"),
                    "green" if len(todos) == 0 else "red",
                )
            )
            if len(todos) == 0:
                print(colored("\nNo TODOs found\n", "blue"))
            else:
                for todo in todos:
                    parts = todo[1].split("#")
                    code = parts[0].strip()
                    comment = parts[1].strip().removeprefix("TODO").strip(":").strip()

                    print(f"\nLine {todo[0] + 1}:")

                    if len(code) > 0:
                        print(colored(code, "red"), end="\n")

                    print(colored("TODO: ", "blue"), end="")
                    print(colored(comment, "yellow"))
                print()
    except Exception as e:
        print(colored(f"Error reading {file_path}: {e}", "yellow"))


def scan_directory_for_todos(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                find_todos_in_file(file_path)

# TODO: Implement abstraction of with(open()) as file
def init():
    """Create file structure for the project"""
    print(os.getcwd())

    # Create folder structure
    create_folder("docs")
    create_folder("src")
    create_folder("tests")

    # TODO: Resolve imports dependent on folder structure

    # python_files = glob.glob('**/*.py', recursive=True)
    # for file in python_files:
    #     print(file)
    #     if file.startswith('test_'):
    #         os.rename(file, f'./tests/{file}')
    #     else:
    #         os.rename(file, f'./src/{file}')

    # Create the init files
    with open("./tests/__init__.py", "a") as f:
        f.write("")
    with open("./src/__init__.py", "a") as f:
        f.write("")

    # Create the env file
    with open("./src/.env", "a") as f:
        f.write("")

    # Create the gitignore file
    with open("./.gitignore", "w") as f:
        f.write("*.pyc\n__pycache__\n.DS_Store\nenv\n.env\n")

    # Create the Dockerfile
    with open("./Dockerfile", "w") as f:
        f.write(
            f'FROM python:{PYTHON_VERSION}\n\nWORKDIR /src\n\nCOPY ./src .\n\nCMD ["python3", "{DEFAULT_PROGRAM_FILE}"]'
        )  # TODO: make sure to update this to the correct file

    # Create the docker compose file
    with open("./docker-compose.yml", "w") as f:
        f.write(
            f'version: "3"\nservices:\n  app:\n    build: .\n    volumes:\n      - .:/src\n    command: python3 {DEFAULT_PROGRAM_FILE}'
        )  # TODO: make sure to update this to the correct file

    # Create the requirements file
    with open("./requirements.txt", "a") as f:
        f.write("")  # update this as things are being added

    # create README file
    with open("./README.md", "w") as f:
        f.write("")  # TODO: update this with the project description

    # create license file
    with open("./LICENSE", "w") as f:
        f.write("")  # TODO: update this with the correct license

def setup():
    os.system("pipreqs --force .")  # TODO: Have a way of noting this dependency


# TODO: Implement for particular file, not ALL files
def todos():
    scan_directory_for_todos("./src")
    scan_directory_for_todos("./tests")

# TODO: Implement for particular file, not ALL files
def format():
    os.system("ruff format ./src")
    os.system("ruff format ./tests")

def create(file_name: str):
    create_file(f"./src/{file_name}", "w", '"""AUTOGENERATED FILE"""')
    create_file(f"./tests/test_{file_name}", "w", '"""AUTOGENERATED TEST FILE"""')

# TODO: Suppress logging
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Invalid input! Please use a proper command.")
        sys.exit(1)

    commands = ['init', 'setup', 'todos', 'format'] # todo: reference coder.txt text file
    actions = ['create']

    command = sys.argv[1]

    file_name = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_PROGRAM_FILE

    if len(sys.argv) > 2 and command not in actions:
        print("Invalid command! Please use a proper command.")
        sys.exit(1)
    elif len(sys.argv) > 2 and command in actions:
        exec(f"{command}('{file_name}')")
        sys.exit(0)
    
    if command not in commands:
        print("Invalid command! Please use a proper command.")
        sys.exit(1)
    elif command in commands:
        exec(f"{command}()")

    

    # change this to run within the docker container
    # try:
    #     exec(open(file_path).read())
    # except Exception as e:
    #     print(f"An error occurred while running the file: {e}")
    #     sys.exit(1)
