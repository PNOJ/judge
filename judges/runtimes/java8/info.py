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
