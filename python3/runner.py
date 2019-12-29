import subprocess

def run(testdata, timeout=None):
    try:
        process = subprocess.run(['python3', 'code.py'], input=testdata, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True, timeout=timeout)
        output = {'data': process.stdout.strip("\n"), 'status': 'EC'}
    except subprocess.TimeoutExpired as e:
        output = {'data': None, 'status': 'TLE'}
    except subprocess.CalledProcessError as e:
        exception_type = e.stderr.strip("\n").split("\n")[-1].split(":")[0]
        output = {'data': exception_type, 'status': 'IR'}
    return output
