from invoke import task

@task(name="html", default=True)
def generate_html(context):
    """API ドキュメントを生成する."""
    commands = """
        rm -r target/sphinx
        sphinx-quickstart target/sphinx -p python-myapp -a AUTHOR -v 0.0.0 -r GA --ext-autodoc --sep -q
        sphinx-apidoc -o target/sphinx/source src/main
        sphinx-build -b html target/sphinx/source target/docs/html
    """.strip().split("\n")

    for command in commands:
        context.run(command)

