from invoke import task

@task(name="unit", iterable=["files"], default=True)
def run_unit_tests(context, files):
    """単体テストを実行する."""
    if files:
        context.run("python -m unittest -v {}".format(" ".join(files)))
    else:
        context.run("python -m unittest discover -v -t . -s src/test")

@task(name="coverage")
def report_unit_test_coverage(context):
    """単体テストのカバレッジをレポートする."""

    commands = """
        coverage erase
        coverage run --branch --omit */src/test/* -m unittest discover -t . -s src/test
        coverage report --include "*/src/main/*"
        coverage html --include "*/src/main/*" --directory=./target/docs/coverage/
    """.strip().split("\n")

    for command in commands:
        context.run(command)

