from invoke import task

@task(name="unit", default=True)
def run_unit_test(context):
    """単体テストを実行する."""
    context.run("python -m unittest discover -s src/test/python -t .")

@task(name="coverage")
def report_unit_test_coverage(context):
    """単体テストのカバレッジをレポートする."""

    commands = """
        python3-coverage erase
        python3-coverage run --omit */src/test/* src/test/python/test_application_version.py
        python3-coverage report
        python3-coverage html
    """.strip().split("\n")

    for command in commands:
        context.run(command)

