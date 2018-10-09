from invoke import task

@task(default=True)
def run(context):
    """
        hello を実行する.
    """
    context.run("python /opt/myapp/current/src/main/myapp/hello/main.py")

@task
def run_webapi(context):
    """
        webapi を実行する.
    """
    context.run("uwsgi --yaml uwsgi.yml")

