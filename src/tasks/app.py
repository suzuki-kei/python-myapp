from invoke import task

@task(default=True)
def run(context):
    """
        hello を実行する.
    """
    context.run("python -m myapp.hello.main")

@task
def run_webapi(context):
    """
        webapi を実行する.
    """
    context.run("uwsgi --yaml uwsgi.yml")

