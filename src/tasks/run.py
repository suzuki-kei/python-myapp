from invoke import task


@task(name="hello", default=True)
def run_hello(context):
    """
        hello を実行する.
    """
    context.run("python -m myapp.hello.main")


@task(name="webapi")
def run_webapi(context):
    """
        webapi を実行する.
    """
    context.run("uwsgi --yaml config/uwsgi.yml")

