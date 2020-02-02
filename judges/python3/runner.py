import subprocess
import time
import psutil

def run(testdata, submission_file_path, time_limit=None, memory_limit=None):
    cpu_time = 0
    memory = 0
    # process = subprocess.run(['python3', submission_file_path], input=testdata, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True, timeout=timeout)
    process = subprocess.Popen(['python3', submission_file_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
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
        exception_type = process.stderr.read().strip("\n").split("\n")[-1].split(":")[0]
        process.stdout.close()
        process.stderr.close()
        output = {'data': exception_type, 'status': 'IR', 'resource': {'time': real_time, 'memory': memory}}
        return output
