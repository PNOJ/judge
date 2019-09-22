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

    def test_running_echo(self):
        problem_src_url = "https://gist.githubusercontent.com/hillcrestpaul0719/c3b3b735a7e083a2598b28c95a26dc6c/raw/problem.json"
        code_src_url = "https://gist.githubusercontent.com/hillcrestpaul0719/c3b3b735a7e083a2598b28c95a26dc6c/raw/test.py"
        testdata_output_url = "https://gist.githubusercontent.com/hillcrestpaul0719/c3b3b735a7e083a2598b28c95a26dc6c/raw/testdata_out.json"

        result = run.main(problem_src_url, code_src_url)
        expected_result_src = requests.get(testdata_output_url)
        expected_result_src.raise_for_status()
        self.assertEqual(result, expected_result_src.json())
