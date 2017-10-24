from invoke import task


@task(default=True)
def test(ctx):
    ctx.run("tox")
