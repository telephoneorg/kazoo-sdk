import os
import glob

from invoke import Collection, task

from . import py, test


collections = [py, test]

ns = Collection()
for c in collections:
    ns.add_collection(c)

ns.configure(dict(
    project='kazoo-sdk',
    pwd=os.getcwd()
))
