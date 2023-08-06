import argparse
import importlib.util
import os.path
import sys
import os

def export(globaldict, package="default"):
    globaldict['ENTRANCEBAR'] = {}
    def __export__(deposit):
        globaldict['ENTRANCEBAR'][package] = deposit
    return __export__

def entrance_file(file, package="default"):
    path = os.path.join(os.path.dirname(os.path.abspath(sys._getframe(1).f_code.co_filename)), file)
    spec = importlib.util.spec_from_file_location(os.path.basename(path), path)
    origin = importlib.util.module_from_spec(spec)
    loaded = spec.loader.exec_module(origin)
    if not 'ENTRANCEBAR' in origin.__dict__:
        return origin
    return origin.__dict__["ENTRANCEBAR"][package]