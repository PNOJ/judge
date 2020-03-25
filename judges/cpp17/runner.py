import subprocess
import time
import os

def run(testdata, submission_file_path, timeout=None):
    try:
        base_dir = os.path.dirname(submission_file_path)
        base_dir_contents = os.listdir(base_dir)
        
        if not "submission" in base_dir_contents:
            subprocess.run(['g++', '-o', 'submission', submission_file_path])
    except subprocess.CalledProcessError as e:
        output = {'data': None, 'status': 'CE'}
        return output
    try:
        start_time = time.time()
        process = subprocess.run(["./submission"], input=testdata, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True, timeout=timeout)
        end_time = time.time()
        duration = end_time - start_time
        output = {'data': process.stdout.strip("\n"), 'status': 'EC', 'time': duration}
    except subprocess.TimeoutExpired as e:
        output = {'data': None, 'status': 'TLE'}
    except subprocess.CalledProcessError as e:
        output = {'data': None, 'status': 'IR'}
    return output
