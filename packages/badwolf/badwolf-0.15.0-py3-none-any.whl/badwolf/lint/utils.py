# -*- coding: utf-8 -*-
import os
from xml.etree import ElementTree


def in_path(name):
    """
    Check whether a command line tool
    exists in the system path.
    """
    for dirname in os.environ['PATH'].split(os.pathsep):
        if os.path.exists(os.path.join(dirname, name)):
            return True
    return False


def npm_exists(name, cwd=None):
    """
    Check whether a cli tool exists in a node_modules/.bin
    dir in os.cwd
    """
    cwd = cwd or os.getcwd()
    path = os.path.join(cwd, 'node_modules', '.bin', name)
    return os.path.exists(path)


def parse_checkstyle(xml):
    tree = ElementTree.fromstring(xml)
    for f in tree.iterfind('file'):
        filename = f.get('name')
        for err in f.iterfind('error'):
            severity = err.get('severity')
            if severity == 'info':
                continue

            line = err.get('line')
            message = err.get('message')
            if ',' in line:
                lines = [int(x) for x in line.split(',') if x != 'undefined']
            else:
                if line == 'undefined':
                    continue
                lines = [int(line)]

            for line in lines:
                yield (filename, line, message)
