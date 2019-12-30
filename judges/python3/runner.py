import subprocess
import time

def run(testdata, submission_file_path, timeout=None):
    try:
        start_time = time.time()
        process = subprocess.run(['python3', submission_file_path], input=testdata, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True, timeout=timeout)
        end_time = time.time()
        duration = end_time - start_time
        output = {'data': process.stdout.strip("\n"), 'status': 'EC', 'time': duration}
    except subprocess.TimeoutExpired as e:
        output = {'data': None, 'status': 'TLE'}
    except subprocess.CalledProcessError as e:
        exception_type = e.stderr.strip("\n").split("\n")[-1].split(":")[0]
        output = {'data': exception_type, 'status': 'IR'}
    return output
