from tempfile import gettempdir
from os.path import exists, join, abspath
import uuid


class File:

    def __init__(self, path):
        self.path = path
        self.position_now = 0

        if not exists(self.path):
            open(self.path, 'w').close()

    def read(self):
        with open(self.path, 'r') as f:
            return f.read()

    def write(self, data):
        with open(self.path, 'w') as f:
            f.write(data)

    def __add__(self, other):
        new_path = join(gettempdir(), str(uuid.uuid4()))
        new_file = type(self)(new_path)
        new_file.write(self.read() + other.read())

        return new_file

    def __str__(self):
        return abspath(self.path)

    def __iter__(self):
        return self

    def __next__(self):
        with open(self.path, 'r') as f:
            f.seek(self.position_now)

            line = f.readline()
            if not line:
                self.position_now = 0
                raise StopIteration('EOF')

            self.current_position = f.tell()

            return line

