from distutils.core import setup
import py2exe
import pandas
import matplotlib

setup(options = {
    "py2exe":
        {
            "includes"      : ["zmq.backend.cython"],
            "excludes"      : ["zmq.libzmq"], 
            "dll_excludes"  : ["MSVCP90.dll",
                               "HID.DLL",
                               "w9xpopen.exe",
                               "libzmq.pyd"],
            "optimize"      : 2
        }
    },
    data_files=matplotlib.get_py2exe_datafiles(),
    windows = [{'script': 'Simple-Time-Series-Viewer.py'}]
    )
