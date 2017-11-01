from invoke import task


@task
def develop(ctx):
    ctx.run("python2 setup.py develop")
    ctx.run("python3 setup.py develop")


@task
def build(ctx):
    ctx.run("python2 setup.py sdist bdist_wheel")
    ctx.run("python3 setup.py sdist bdist_wheel")


@task
def upload(ctx):
    ctx.run("twine upload dist/*")


@task
def clean(ctx):
    ctx.run("rm -rf build dist *.egg-info **/.pyc **/__pycache__")


@task(build, upload, clean)
def publish(ctx):
    pass
