import os
from unittest import TestLoader
from unittest import TextTestRunner

from coverage import Coverage
from invoke import task

def _run_unit_tests():
    test_suite = TestLoader().discover("/app/src/test/python", "test_*.py", ".")
    TextTestRunner().run(test_suite)

@task(name="unit", default=True)
def run_unit_tests(context):
    """単体テストを実行する."""
    _run_unit_tests()

@task(name="coverage")
def report_unit_test_coverage(context):
    """単体テストのカバレッジをレポートする."""
    coverage = Coverage()
    coverage.set_option("run:branch", True)
    coverage.erase()
    coverage.start()
    _run_unit_tests()
    coverage.stop()
    coverage.save()
    coverage.report(include="*/src/main/*")
    coverage.html_report(include="*/src/main/*", directory="./target/docs/coverage")

