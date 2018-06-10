from invoke import task

@task(default=True)
def run(context):
    """
        アプリケーションを実行する.
    """
    context.run("python /app/src/main/python/myapp/hello/main.py")

