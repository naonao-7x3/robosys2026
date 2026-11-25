# SPDX-FileCopyrightText: 2026 Naomi Miura
# SPDX-License-Identifier: BSD-3-Clause

import pathlib
import subprocess
import unittest


COMMAND = pathlib.Path(__file__).resolve().parents[1] / "rangefilter"


class RangeFilterTests(unittest.TestCase):
    def run_command(self, args, input_text=""):
        return subprocess.run(
            [str(COMMAND), *args],
            input=input_text,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_outputs_only_values_outside_inclusive_range(self):
        result = self.run_command(["0", "10"], "-2\n0\n5\n10\n12\n")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "-2\n12\n")
        self.assertEqual(result.stderr, "")

    def test_accepts_comma_separated_values_and_comments(self):
        result = self.run_command(["1", "5"], "0, 2, 6 # sensor A\n3\n")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "0\n6\n")

    def test_all_values_in_range_produces_no_output(self):
        result = self.run_command(["1", "5"], "1 2 3 4 5\n")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, "")

    def test_empty_input_produces_no_output(self):
        result = self.run_command(["0", "10"])
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")

    def test_non_numeric_input_fails_without_partial_output(self):
        result = self.run_command(["0", "10"], "-1\nabc\n11\n")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        self.assertIn("数値でない値", result.stderr)

    def test_non_finite_measurement_fails(self):
        result = self.run_command(["0", "10"], "nan\n")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        self.assertIn("有限でない値", result.stderr)

    def test_missing_argument_fails(self):
        result = self.run_command(["0"])
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("使い方", result.stderr)

    def test_reversed_limits_fail(self):
        result = self.run_command(["10", "0"], "5\n")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("下限は上限以下", result.stderr)

    def test_non_finite_limit_fails(self):
        result = self.run_command(["-inf", "10"], "5\n")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("有限の数値", result.stderr)


if __name__ == "__main__":
    unittest.main()
