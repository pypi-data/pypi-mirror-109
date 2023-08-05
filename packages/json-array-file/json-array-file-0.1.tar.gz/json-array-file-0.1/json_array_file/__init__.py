import json


class JsonArrayFileWriter:
    def __init__(self, filepath, indent=None):
        self.filepath = filepath
        self.indent = indent
        self.lines = 0
        with open(filepath, 'w') as f:
            f.write('[')

    def write_dict(self, dct: dict) -> None:
        jsn = json.dumps(dct, indent=self.indent)
        with open(self.filepath, 'a') as f:
            f.write(',\n') if self.lines else f.write('\n')
            f.write(jsn)
        self.lines += 1

    def close(self) -> None:
        with open(self.filepath, 'a') as f:
            f.write('\n')
            f.write(']')
