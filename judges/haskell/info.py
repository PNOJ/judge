import os

language_code = "haskell"

file_ext = ".hs"

def garbage_collector():
    os.remove("submission.hs")
    os.remove("submission.o")
    os.remove("submission.hi")
    if "submission" in os.listdir():
        os.remove("submission")
