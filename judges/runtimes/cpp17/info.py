import os

language_code = "c++17"

file_ext = ".cpp"

def garbage_collector():
    os.remove("submission.cpp")
    if "submission" in os.listdir():
        os.remove("submission")

def name_submission(submission_content):
    return "submission.cpp"

def compile_command(file_name):
    return ['g++', '-o', 'submission', file_name]

def binary_name(file_name):
    return "submission"

def run_command(file_name):
    return ["./{0}".format(file_name)]
