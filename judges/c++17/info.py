import os

language_code = "c++17"

file_ext = ".cpp"

def garbage_collector():
    os.remove("submission.cpp")
    if "submission" in os.listdir():
        os.remove("submission")
