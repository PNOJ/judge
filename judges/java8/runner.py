import subprocess
import time
import re
import os
import shutil
import psutil
import sys

public_class_regex = re.compile(r'public class ([^ \n]*)')

def get_public_class_name(submission_file_path):
    base_dir = os.path.dirname(submission_file_path)
    base_dir_contents = os.listdir(base_dir)

    submission_file = open(submission_file_path, "r")
    submission_code = submission_file.read()
    submission_file.close()
    public_class_match = re.search(public_class_regex, submission_code)        

    return public_class_match.group(1)

def get_new_submission_file_name(submission_file_path):
    public_class_name = get_public_class_name(submission_file_path)

    new_submission_file_name = "{}.java".format(public_class_name)
    new_submission_file_path = os.path.join(os.path.dirname(submission_file_path), new_submission_file_name)

    return new_submission_file_path

def get_new_compiled_submission_file_name(submission_file_path):
    public_class_name = get_public_class_name(submission_file_path)

    new_compiled_submission_file_name = "{}.class".format(public_class_name)
    return new_compiled_submission_file_name

def get_new_compiled_submission_file_path(submission_file_path):
    new_compiled_submission_file_name = get_new_compiled_submission_file_name(submission_file_path)
    new_compiled_submission_file_path = os.path.join(os.path.dirname(submission_file_path), new_compiled_submission_file_name)

    return new_compiled_submission_file_path

def get_new_compiled_submission_class_name(submission_file_path):
    new_compiled_submission_file_name = get_new_compiled_submission_file_name(submission_file_path)
    return new_compiled_submission_file_name[:-6]

def compile_submission(submission_file_path):
    new_submission_file_path = get_new_submission_file_name(submission_file_path)

    shutil.copyfile(submission_file_path, new_submission_file_path)
    try:
        compile_process = subprocess.run(['javac', new_submission_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, timeout=10)
    except subprocess.TimeoutExpired:
        return {'message': 'Compilation Timed Out', 'status': 'CE'}
    os.remove(new_submission_file_path)

    stdout = compile_process.stdout
    stderr = compile_process.stderr

    if compile_process.returncode == 0:
        return {'status': 'CC'}
    else:
        output = {'message': stderr, 'status': 'CE'}
        return output

def run(testdata, submission_file_path, time_limit=None, memory_limit=None):
    new_compiled_submission_class_name = get_new_compiled_submission_class_name(submission_file_path)

    cpu_time = 0
    memory = 0
    # process = subprocess.run(['java', public_class_match.group(1)], input=testdata, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True, timeout=timeout)
    process = subprocess.Popen(['java', new_compiled_submission_class_name], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    process.stdin.write(testdata)
    process.stdin.close()
    real_start_time = time.time()
    while process.poll() == None:
        process_info = psutil.Process(pid=process.pid)
        process_cpu_time_info = process_info.cpu_times()
        cpu_time = process_cpu_time_info.user + process_cpu_time_info.system
        process_memory_info = process_info.memory_info()
        memory = max(memory, process_memory_info.rss / (1024**2))
        real_time = time.time() - real_start_time
        
        if time_limit != None and real_time > time_limit:
            output = process.stdout.read()
            process.stdout.close()
            process.stderr.close()
            process.kill()
            result = {'output': None, 'status': 'TLE', 'resource': {'time': real_time, 'memory': memory}}
            return result
        elif memory_limit != None and memory > memory_limit:
            process.stdout.close()
            process.stderr.close()
            process.kill()
            result = {'output': None, 'status': 'MLE', 'resource': {'time': real_time, 'memory': memory}}
            return result
    
    if process.returncode == 0:
        output = process.stdout.read()
        process.stdout.close()
        process.stderr.close()
        if sys.getsizeof(output) > 67108864:
            result = {'output': None, 'status': 'OLE', 'resource': {'time': real_time, 'memory': memory}}
        else:
            result = {'output': output.strip("\n"), 'status': 'EC', 'resource': {'time': real_time, 'memory': memory}}
        return result
    else:
        process.stdout.close()
        process.stderr.close()
        result = {'output': None, 'status': 'IR', 'resource': {'time': real_time, 'memory': memory}}
        return result
