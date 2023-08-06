import tempfile
import os
import json
import sys
import shutil
import pathlib

__all__ = [
    "JsonHandler",
    "TempHandler"
]


class JsonHandler:
    def __init__(self, file=None):
        self.file = file

    def load(self):
        with open(self.file, 'r') as loaded:
            return json.load(loaded)

    def dump(self, store):
        with open(self.file, 'w') as loaded:
            return json.dump(store, loaded, indent=4)

    def __call__(self, raw: str):
        return json.loads(raw)


class TempHandler:
    def __init__(self, *args, **kwargs):
        self.note = []

    def __call__(self, suffix='', prefix='', dir_=None, text=True):
        mode, file = tempfile.mkstemp(suffix, prefix, dir_, text)
        os.close(mode)
        self.note.append(file)
        return file

    def close(self):
        return [os.remove(_) for _ in self.note if os.path.exists(_)]

    def make_temp(self, path=None):
        path = os.path.dirname(__file__) if not path else path if os.path.isdir(path) else os.path.dirname(path)
        temp = os.path.join(path, "temp")
        os.mkdir(temp)
        return temp


def export_rash(current_path):
    if not os.path.isdir(current_path):
        raise NotADirectoryError(f"{current_path} is not a directory")
