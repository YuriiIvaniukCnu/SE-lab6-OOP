import os
import subprocess
import sys
import unittest

from lab6 import (Employee, HourlyEmployee, FixedEmployee, FOPEmployee, SelfEmployed,
                  generate_employees, sort_employees)

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lab6.py")


def run_cli(*args):
    result = subprocess.run([sys.executable, SCRIPT, *args], capture_output=True, text=True)
    return result.returncode, [line.split() for line in result.stdout.splitlines()]


class TestEmployees(unittest.TestCase):
    def test_abstract(self):
        with self.assertRaises(TypeError):
            Employee("1", "Петренко")
    def test_hourly(self):
        e = HourlyEmployee("1", "Петренко", 100)
        self.assertAlmostEqual(e.salary(), 16640)
        self.assertAlmostEqual(e.tax(), 3244.8)
    def test_fixed(self):
        e = FixedEmployee("1", "Петренко", 20000)
        self.assertEqual(e.salary(), 20000)
        self.assertAlmostEqual(e.tax(), 3900)
    def test_fop(self):
        e = FOPEmployee("1", "Петренко", 100, 3)
        self.assertAlmostEqual(e.salary(), 18304)
        self.assertAlmostEqual(e.tax(), 18304 * 0.05 + 1760)
    def test_self_employed(self):
        e = SelfEmployed("1", "Петренко", 10, 2000)
        self.assertEqual(e.salary(), 20000)
        self.assertAlmostEqual(e.tax(), 3900 + 1760)
    def test_sort(self):
        a = FixedEmployee("1", "Шевченко", 20000)
        b = FixedEmployee("2", "Бондар", 20000)
        c = FixedEmployee("3", "Яценко", 30000)
        self.assertEqual(sort_employees([a, b, c]), [c, b, a])
    def test_generate(self):
        self.assertEqual(len(generate_employees(10)), 10)


class TestCLI(unittest.TestCase):
    def test_all(self):
        code, rows = run_cli()
        self.assertEqual(code, 0)
        self.assertEqual(len(rows), 20)
    def test_group(self):
        code, rows = run_cli("group", "3")
        self.assertEqual(code, 0)
    def test_wrong_group(self):
        self.assertEqual(subprocess.call([sys.executable, SCRIPT, "group", "5"], stderr=subprocess.DEVNULL), 2)
    def test_income(self):
        code, rows = run_cli("income", "80000")
        self.assertEqual(code, 0)
        for row in rows:
            self.assertGreaterEqual(float(row[-2]), 80000)
    def test_tax(self):
        code, rows = run_cli("tax", "5000")
        self.assertEqual(code, 0)
        for row in rows:
            self.assertGreaterEqual(float(row[-1]), 5000)


if __name__ == '__main__':
    unittest.main()
