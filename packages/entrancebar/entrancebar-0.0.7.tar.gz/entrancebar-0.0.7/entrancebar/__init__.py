import argparse
import importlib.util
import os.path
import sys
import os
import os.path
from mako.template import Template

alias = {}

if os.path.exists(os.path.join(os.getcwd(), "./entrancebar.config.json")):
    try:
        import ujson as json
    except ModuleNotFoundError:
        import json
    context = json.load(open(os.path.join(os.getcwd(), "./entrancebar.config.json")))
    alias = context.get("alias", {})

def export(globaldict, package="default"):
    globaldict['ENTRANCEBAR'] = {}
    def __export__(deposit):
        globaldict['ENTRANCEBAR'][package] = deposit
    return __export__

def entrance_file(filename: str, package="default"):
    for i in alias.keys():
        filename = filename.replace(i, alias[i])
    filename = Template(filename).render(projectDir=os.getcwd())
    path = os.path.join(os.path.dirname(os.path.abspath(sys._getframe(1).f_code.co_filename)), filename)
    spec = importlib.util.spec_from_file_location(os.path.basename(path), path)
    origin = importlib.util.module_from_spec(spec)
    loaded = spec.loader.exec_module(origin)
    if 'ENTRANCEBAR' not in origin.__dict__:
        return origin
    return origin.__dict__["ENTRANCEBAR"][package]