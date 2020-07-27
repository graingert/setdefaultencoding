# -*- coding: ascii -*-
import os.path
import sys
import tempfile
from distutils.command.build import build

from setuptools import setup

py2_files = {
    "setdefaultencoding.pth": (
        b"import sys; "
        b"import setdefaultencoding; "
        b"setdefaultencoding.setdefaultencoding = sys.setdefaultencoding"
    ),
    "setdefaultencoding.py": (
        b"def setdefaultencoding(*args, **kwargs): "
        b'raise Exception("setdefaultencoding.pth file was not installed/run!")'
    ),
}

py3_files = {"setdefaultencoding.py": b"def setdefaultencoding(*args, **kwargs): pass"}

files = sorted((py3_files if sys.version_info >= (3,) else py2_files).items())


class BuildWithPTH(build):
    def run(self):
        build.run(self)
        for dfn, content in files:
            with tempfile.NamedTemporaryFile() as f:
                f.write(content)
                f.flush()
                self.copy_file(f.name, os.path.join(self.build_lib, dfn))


setup(cmdclass={"build": BuildWithPTH})
