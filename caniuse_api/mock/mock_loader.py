import json
import os

_base_dir = os.path.abspath(os.path.dirname(__file__))


def load_mock(name):
    file_path = os.path.join(_base_dir, 'data/%s.json' % name)
    with open(file_path) as data_file:
        data = json.load(data_file)
        return data
