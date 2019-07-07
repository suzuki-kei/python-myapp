from invoke import task

@task(name="html", default=True)
def generate_html(context):
    """API ドキュメントを生成する."""
    commands = """
        sphinx-apidoc -fF --ext-viewcode --extensions sphinx.ext.napoleon -o target/sphinx src/main
        sphinx-build -anW --keep-going -Dautodoc_default_flags=private-members target/sphinx target/docs/html
    """.strip().split("\n")

    for command in commands:
        context.run(command)

