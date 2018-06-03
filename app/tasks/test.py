import os
from unittest import TestLoader
from unittest import TextTestRunner

from coverage import Coverage
from invoke import task

@task(name="unit", default=True)
def run_unit_tests(context):
    """単体テストを実行する."""
    context.run("python -m runner")

@task(name="coverage")
def report_unit_test_coverage(context):
    """単体テストのカバレッジをレポートする."""

    commands = """
        coverage erase
        coverage run --branch --omit */src/test/* -m runner
        coverage report --include "*/src/main/*"
        coverage html --include "*/src/main/*" --directory=./target/docs/coverage/
    """.strip().split("\n")

    for command in commands:
        context.run(command)

