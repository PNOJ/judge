import unittest
import judge
import copy
import shutil
import os
import requests
import yaml

class JudgeTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def tearDown(self):
        shutil.rmtree("./problem")
        os.remove("problem.zip")
        os.remove("submission.py")

    def fetch_problem_and_test(self, problem_root, language, solution_status):
        problem_root = problem_root.strip("/")

        args = {}
        args['problem_file_url'] = "{0}/problem.zip".format(problem_root)
        args['submission_file_url'] = "{0}/solutions/{1}/{2}/solution.py".format(problem_root, language, solution_status)
        args['callback_url'] = 'https://example.com/callback'

        try:
            expected_result = requests.get("{0}/solutions/{1}/{2}/result.json".format(problem_root, language, solution_status))
            expected_result.raise_for_status()
            expected_result = expected_result.json()
        except requests.exceptions.HTTPError:
            expected_result = None

        result = judge.main(args)

        if expected_result == None:
            print(result)
            return

        problem_manifest_file = open("problem/manifest.yaml", "r")
        problem_manifest = yaml.safe_load(problem_manifest_file)
        problem_manifest_file.close()
        time_limit = problem_manifest['metadata']['limit']['time']

        for batch in range(0, len(expected_result['batches'])):
            for testcase in range(0, len(expected_result['batches'][batch]['testcases'])):
                if expected_result['batches'][batch]['testcases'][testcase]['status'] in ['AC', 'WA']:
                    self.assertTrue(expected_result['batches'][batch]['testcases'][testcase]['time'] <= time_limit)
                    del expected_result['batches'][batch]['testcases'][testcase]['time']
                    del result['batches'][batch]['testcases'][testcase]['time']

        self.assertEqual(expected_result, result)

    def test_helloworld_ac(self):
        self.fetch_problem_and_test("https://paullee-cdn.nyc3.digitaloceanspaces.com/pnoj/problems/helloworld/", "py3", "ac")

    def test_aplusb_ac(self):
        self.fetch_problem_and_test("https://paullee-cdn.nyc3.digitaloceanspaces.com/pnoj/problems/aplusb/", "py3", "ac")

    def test_aplusb_wa(self):
        self.fetch_problem_and_test("https://paullee-cdn.nyc3.digitaloceanspaces.com/pnoj/problems/aplusb/", "py3", "wa")

    def test_aplusb_tle(self):
        self.fetch_problem_and_test("https://paullee-cdn.nyc3.digitaloceanspaces.com/pnoj/problems/aplusb/", "py3", "tle")

    def test_aplusb_ir(self):
        self.fetch_problem_and_test("https://paullee-cdn.nyc3.digitaloceanspaces.com/pnoj/problems/aplusb/", "py3", "ir")

if __name__ == "__main__":
    unittest.main()
