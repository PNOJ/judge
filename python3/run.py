import sys
import json
import subprocess
import requests

def run(testdata, timeout=None):
    process = subprocess.Popen(['python3', 'code.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        stdout, stderr = process.communicate(input=testdata, timeout=timeout)
        output = {'data': stdout.strip("\n"), 'status': 'EC'}
    except subprocess.TimeoutExpired:
        process.terminate()
        process.wait(timeout=3)
        process.stdout.close()
        process.stderr.close()
        output = {'data': None, 'status': 'TLE'}
    return output

def main(problem_src_url, code_src_url, result_submission_url=None, communication_key=None):
    if communication_key == None:
        auth = None
    else:
        auth = ('judge', communication_key)

    code_src = requests.get(code_src_url, auth=auth)
    code_src.raise_for_status()
    code_file = open("code.py", "w")
    code_file.write(code_src.text)
    code_file.close()

    problem_src = requests.get(problem_src_url, auth=auth)
    problem_src.raise_for_status()
    problem = problem_src.json()
    assert problem['type'] == 'problem'

    problem_name = problem['name']
    problem_points = problem['points']
    problem_timelimit = problem['timelimit']
    problem_memorylimit = problem['memorylimit']
    problem_allowedlanguages = problem['allowedlanguages']
    problem_testdata_input_url = problem['testdata_input_url']

    testdata_src = requests.get(problem_testdata_input_url, auth=auth)
    testdata_src.raise_for_status()
    testdata = testdata_src.json()
    assert testdata['type'] == 'testdata_input'
    assert testdata['problem'] == problem_name

    results = []
    for i in testdata['testcases']:
        result = run(i['data'], problem_timelimit)
        result['id'] = i['id']
        results.append(result)

    response = {
        'type': 'testdata_output',
        'problem': problem_name,
        'testcases': results
    }

    if result_submission_url == None:
        return response
    else:
        requests.post(result_submission_url, json=response, auth=auth)

if __name__ == "__main__":
    problem_src_url = sys.argv[1]
    code_src_url = sys.argv[2]
    result_submission_url = sys.argv[3]
    if len(sys.argv) > 4:
        communication_key = sys.argv[4]
    else:
        communication_key = None

    main(problem_src_url, code_src_url, result_submission_url, communication_key)
