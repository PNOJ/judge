import argparse
import requests
import os
import zipfile
import pyyaml

def download(url, path):
    res = requests.get(url)
    res.raise_for_status()
    file_obj = open(path, "wb")
    for chunk in res.iter_content(100000):
        file_obj.write(chunk)
    file_obj.close()

def main(args):
    download(args['problem_file_url'], "problem.zip")
    download(args['submission_file_url']. "submission.py")

    with zipfile.ZipFile("problem.zip", "r") as zip_ref:
        zip_ref.extractall("problem")

    os.rename("runner.py", "problem/runner.py")

    problem_manifest_file = open("problem/manifest.yaml", "r")
    problem_manifest = pyyaml.safe_load(problem_manifest_file)
    problem_manifest_file.close()

    grader_args = problem_manifest['judge']['args']
    grader_args['submission_file'] = os.path.abspath("submission.py")
    grader_args['timeout'] = problem_manifest['metadata']['limit']['time']
    grader = __import__('problem/grader.py')
    try:
        submission_result = grader.main(grader_args)
    except Exception as e:
        traceback.print_exc()
        submission_result = {'status': 'IE'}

    request = requests.post(args['callback_url'], json=submission_result)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args = vars(parser.parse_args())
    result = main(args)
    result_json = json.dumps(result)
    print(result_json)
