import json
import os.path


def load_fixture(filename):
    full_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        "fixtures", filename
    )
    with open(full_path) as fd:
        return fd.read()


def load_fixture_as_dict(filename):
    return json.loads(load_fixture(filename))
