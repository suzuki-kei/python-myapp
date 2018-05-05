from invoke import task

@task(default=True)
def run(context):
    """
        アプリケーションを実行する.
    """
    context.run("python src/main/python/application.py")

