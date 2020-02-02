import unittest
import judge
import copy
import shutil
import os
import requests
import yaml
import info
import json

problems_root = "https://paullee-cdn.nyc3.digitaloceanspaces.com/pnoj/problems/"

class JudgeTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def tearDown(self):
        shutil.rmtree("./problem")
        os.remove("problem.zip")
        
        info.garbage_collector()

    def fetch_problem_and_test(self, problems_root, problem_name, language, solution_status):
        problem_root = "{0}/{1}".format(problems_root.strip("/"), problem_name)

        args = {}
        args['problem_file_url'] = "{0}/problem.zip".format(problem_root)
        args['submission_file_url'] = "{0}/solutions/{1}/{2}/solution{3}".format(problem_root, language, solution_status, info.file_ext)
        args['callback_url'] = 'https://example.com/callback'

        try:
            expected_result = requests.get("{0}/solutions/{1}/{2}/result.json".format(problem_root, language, solution_status))
            expected_result.raise_for_status()
            expected_result = expected_result.json()
        except requests.exceptions.HTTPError:
            expected_result = None

        result = judge.main(args)
        orig_result = copy.deepcopy(result)

        if expected_result == None:
            print(result)
            return

        problem_manifest_file = open("problem/manifest.yaml", "r")
        problem_manifest = yaml.safe_load(problem_manifest_file)
        problem_manifest_file.close()
        time_limit = problem_manifest['metadata']['limit']['time']
        memory_limit = problem_manifest['metadata']['limit']['memory']

        try:
            del expected_result['resource']
        except KeyError:
            print("Resource field is not found on the expected result.")
        del result['resource']

        for batch in range(0, len(expected_result['batches'])):
            try:
                del expected_result['batches'][batch]['resource']
            except KeyError:
                print("Resource field is not found on the expected result.")
            del result['batches'][batch]['resource']

            for testcase in range(0, len(expected_result['batches'][batch]['testcases'])):
                if result['batches'][batch]['testcases'][testcase]['status'] in ['AC', 'WA', 'IR']:
                    self.assertTrue(result['batches'][batch]['testcases'][testcase]['resource']['time'] <= time_limit)
                    self.assertTrue(result['batches'][batch]['testcases'][testcase]['resource']['memory'] <= memory_limit)
                if result['batches'][batch]['testcases'][testcase]['status'] == 'TLE':
                    self.assertTrue(result['batches'][batch]['testcases'][testcase]['resource']['time'] >= time_limit)
                    self.assertTrue(result['batches'][batch]['testcases'][testcase]['resource']['memory'] <= memory_limit)
                if result['batches'][batch]['testcases'][testcase]['status'] == 'MLE':
                    self.assertTrue(result['batches'][batch]['testcases'][testcase]['resource']['time'] <= time_limit)
                    self.assertTrue(result['batches'][batch]['testcases'][testcase]['resource']['memory'] >= memory_limit)

                try:
                    del expected_result['batches'][batch]['testcases'][testcase]['resource']
                except KeyError:
                    print("Resource field is not found on the expected result.")
                del result['batches'][batch]['testcases'][testcase]['resource']

        if not expected_result == result:
            print(json.dumps(orig_result))
        self.assertEqual(expected_result, result)

    def test_helloworld_ac(self):
        self.fetch_problem_and_test(problems_root, "helloworld", info.language_code, "ac")

    def test_aplusb_ac(self):
        self.fetch_problem_and_test(problems_root, "aplusb", info.language_code, "ac")

    def test_aplusb_wa(self):
        self.fetch_problem_and_test(problems_root, "aplusb", info.language_code, "wa")

    def test_aplusb_tle(self):
        self.fetch_problem_and_test(problems_root, "aplusb", info.language_code, "tle")

    def test_aplusb_mle(self):
        self.fetch_problem_and_test(problems_root, "aplusb", info.language_code, "mle")

    def test_aplusb_ir(self):
        self.fetch_problem_and_test(problems_root, "aplusb", info.language_code, "ir")

if __name__ == "__main__":
    unittest.main()
