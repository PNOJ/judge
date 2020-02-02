import subprocess
import time
import re
import os
import shutil
import psutil

public_class_regex = re.compile(r'public class ([^ \n]*)')

def run(testdata, submission_file_path, time_limit=None, memory_limit=None):
    try:
        base_dir = os.path.dirname(submission_file_path)
        base_dir_contents = os.listdir(base_dir)

        submission_file = open(submission_file_path, "r")
        submission_code = submission_file.read()
        submission_file.close()
        public_class_match = re.search(public_class_regex, submission_code)        

        new_submission_file_name = "{}.java".format(public_class_match.group(1))
        new_submission_file_path = os.path.join(os.path.dirname(submission_file_path), new_submission_file_name)

        new_compiled_submission_file_name = "{}.class".format(public_class_match.group(1))
        new_compiled_submission_file_path = os.path.join(os.path.dirname(submission_file_path), new_compiled_submission_file_name)


        if not new_compiled_submission_file_name in base_dir_contents:
            shutil.copyfile(submission_file_path, new_submission_file_path)
            subprocess.run(['javac', new_submission_file_path])
            os.remove(new_submission_file_path)
    except subprocess.CalledProcessError as e:
        print(str(e))
        output = {'data': None, 'status': 'CE'}
        return output
    cpu_time = 0
    memory = 0
    # process = subprocess.run(['java', public_class_match.group(1)], input=testdata, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True, timeout=timeout)
    process = subprocess.Popen(['java', public_class_match.group(1)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
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
            process.stdout.close()
            process.stderr.close()
            process.kill()
            output = {'data': None, 'status': 'TLE', 'resource': {'time': real_time, 'memory': memory}}
            return output
        elif memory_limit != None and memory > memory_limit:
            process.stdout.close()
            process.stderr.close()
            process.kill()
            output = {'data': None, 'status': 'MLE', 'resource': {'time': real_time, 'memory': memory}}
            return output
    
    if process.returncode == 0:
        output = {'data': process.stdout.read().strip("\n"), 'status': 'EC', 'resource': {'time': real_time, 'memory': memory}}
        process.stdout.close()
        process.stderr.close()
        return output
    else:
        process.stdout.close()
        process.stderr.close()
        output = {'data': None, 'status': 'IR', 'resource': {'time': real_time, 'memory': memory}}
        return output
