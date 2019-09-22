import unittest
import os
import requests

try:
    from python3 import run
except ModuleNotFoundError:
    import run

class TestRun(unittest.TestCase):
    def tearDown(self):
        # Clean up
        os.remove('./code.py')

    def run_and_compare_with_expected_output(self, problem_src_url, code_src_url, testdata_output_url):
        result = run.main(problem_src_url, code_src_url)
        expected_result_src = requests.get(testdata_output_url)
        expected_result_src.raise_for_status()
        self.assertEqual(result, expected_result_src.json())

    def test_running_echo(self):
        # https://gist.github.com/hillcrestpaul0719/c3b3b735a7e083a2598b28c95a26dc6c

        base_url = "https://gist.githubusercontent.com/hillcrestpaul0719/c3b3b735a7e083a2598b28c95a26dc6c/raw/"
        problem_src_url = base_url + "echo_problem.json"
        code_src_url = base_url + "test.py"
        testdata_output_url = base_url + "testdata_out.json"

        self.run_and_compare_with_expected_output(problem_src_url, code_src_url, testdata_output_url)

    def test_running_timeout(self):
        # https://gist.github.com/hillcrestpaul0719/1b7993abd01aadc6bb281f853670ea1c

        base_url = "https://gist.githubusercontent.com/hillcrestpaul0719/1b7993abd01aadc6bb281f853670ea1c/raw/"
        problem_src_url = base_url + "timeout_problem.json"
        code_src_url = base_url + "addition.py"
        testdata_output_url = base_url + "testdata_out.json"

        self.run_and_compare_with_expected_output(problem_src_url, code_src_url, testdata_output_url)
