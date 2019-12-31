import subprocess
import time
import re
import os
import shutil

public_class_regex = re.compile(r'public class ([^ \n]*)')

def run(testdata, submission_file_path, timeout=None):
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
    try:
        start_time = time.time()
        process = subprocess.run(['java', public_class_match.group(1)], input=testdata, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True, timeout=timeout)
        end_time = time.time()

        duration = end_time - start_time
        output = {'data': process.stdout.strip("\n"), 'status': 'EC', 'time': duration}
    except subprocess.TimeoutExpired as e:
        output = {'data': None, 'status': 'TLE'}
    except subprocess.CalledProcessError as e:
        output = {'data': None, 'status': 'IR'}

    return output
