import os

language_code = "py3"

file_ext = ".py"

def garbage_collector():
    os.remove("submission.py")

def name_submission(submission_content):
    return "submission.py"

def compile_command(file_name):
    return ["python3", "-m", "py_compile", submission_file_path]

def binary_name(file_name):
    return file_name

def run_command(file_name):
    return ["python3", file_name]
