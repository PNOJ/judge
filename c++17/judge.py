import argparse
import requests
import os
import zipfile
import yaml
import shutil
import traceback

def download(url, path):
    res = requests.get(url)
    res.raise_for_status()
    file_obj = open(path, "wb")
    for chunk in res.iter_content(100000):
        file_obj.write(chunk)
    file_obj.close()

def main(args):
    download(args['problem_file_url'], "problem.zip")
    download(args['submission_file_url'], "submission.cpp")

    with zipfile.ZipFile("problem.zip", "r") as zip_ref:
        zip_ref.extractall("problem")

    problem_manifest_file = open("problem/manifest.yaml", "r")
    problem_manifest = yaml.safe_load(problem_manifest_file)
    problem_manifest_file.close()

    grader_args = problem_manifest['judge']['args']
    grader_args['submission_file'] = os.path.abspath("submission.cpp")
    grader_args['timeout'] = problem_manifest['metadata']['limit']['time']
    grader_args['grader_base_path'] = os.path.join(os.path.dirname(__file__), "problem")

    if 'url' in problem_manifest['judge']['grader']:
        download(problem_manifest['judge']['grader']['url'], "problem/grader.py")       
    elif 'file' in problem_manifest['judge']['grader']:
        os.rename('problem/{}'.format(problem_manifest['judge']['grader']['file']), 'problem/grader.py')
    else:
        download("https://paullee-cdn.nyc3.digitaloceanspaces.com/pnoj/graders/standard.py", "problem/grader.py")       

    shutil.copyfile("files/__init__.py", "problem/__init__.py")

    problem = __import__('problem')
    try:
        submission_result = problem.grader(grader_args)
    except Exception as e:
        traceback.print_exc()
        submission_result = {'status': 'IE', 'data': str(e)}

    return submission_result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args = vars(parser.parse_args())
    result = main(args)
    request = requests.post(args['callback_url'], json=result)
    result_json = json.dumps(result)
    print(result_json)
