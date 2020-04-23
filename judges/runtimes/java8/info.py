import os
import re

language_code = "java8"

file_ext = ".java"

compiled_file_name_regex = re.compile(r".*\.class")

def garbage_collector():
    os.remove("submission.java")
    dir_contents = os.listdir()
    for i in dir_contents:
        if not re.match(compiled_file_name_regex, i) == None:
            os.remove(i)

public_class_regex = re.compile(r'public class ([^ \n-/\\{}"\'`~<>]*)')

def name_submission(submission_content):
    public_class_match = re.search(public_class_regex, submission_content)
    return "{0}.java".format(public_class_match)

def compile_command(file_name):
    return ['javac', file_name]

def binary_name(file_name):
    return file_name[:-5]

def run_command(file_name):
    return ['java', file_name]
