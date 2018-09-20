# -*- coding: utf-8 -*-
# __author__ = 'Gz'
import json


def to_har_json(path, new_path):
    with open(path, 'r') as old:
        new = json.load(old)
        print(new)
    with open(new_path, 'w') as har:
        har.write(str(new))


if __name__ == "__main__":
    to_har_json('./gz', './gz.har')
