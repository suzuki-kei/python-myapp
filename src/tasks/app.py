from invoke import task

@task(default=True)
def run(context):
    """
        アプリケーションを実行する.
    """
    context.run("python /opt/myapp/current/src/main/myapp/hello/main.py")

