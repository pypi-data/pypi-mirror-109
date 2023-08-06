"""
Package: CompressPNG
"""
__author__  = "Xia Clark <joehisaishi1943@gmail.com>"

from distutils.core      import setup
from distutils.sysconfig import get_python_lib
import sys
import os
import shutil
import subprocess
import platform

CLASSIFIERS = """
Development Status :: 5 - Production/Stable
Programming Language :: Python
Topic :: Software Development :: Testing
"""[1:-1]

DESCRIPTION = """
CompressPNG a Robot Framework keyword library wrapper just for PNG compressing purpose.
"""[1:-1]

if __name__ == "__main__":
    #
    # Do the distutils installation
    #
    setup(name         = "CompressPNG",
          version      = "0.2",
          description  = "Compress PNG for Robot Framework screenshot",
          author       = "Joe Hisaishi",
          author_email = "joehisaishi1943@gmail.com",
          url          = "https://github.com/lucyking/CompressPNG",
          license      = "GPLv2",
          platforms    = "all",
          classifiers  = CLASSIFIERS.splitlines(),
          long_description = DESCRIPTION,
          package_dir  = {'' : "src"},
          packages     = ["CompressPNG"],
          install_requires = ['pillow'],
          data_files   = []
         )
#
# -------------------------------- End of file --------------------------------
