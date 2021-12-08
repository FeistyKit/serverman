#!/usr/bin/env python

import zerorpc, os, re, pathlib
from typing import Optional
from dataclasses import dataclass

HOME_DIR = os.environ['HOME']

# If file exists
def fexists(path: str) -> bool:
    return pathlib.Path(path).is_file()

# if dire exists
def dexists(path: str) -> bool:
    return pathlib.Path(path).is_dir()

class ServerManager(object):
    pass

# detect the type of project and automatically make a config file for it
# TODO: customizable default yaml
def generate_config_file(path: str, lang_type: Optional[str] =None):
    yaml = ""
    with open(path, "w") as f:
        f.write("# this file was generated automatically by serverman. <https://www.github.com/FeistyKit/serverman> Modify it as you wish!")
    info = find_proj_info(lang_type)


@dataclass
class ProjInfo:
    build_command: Optional[str]
    proj_name: Optional[str]
    execut_command: Optional[str] # path to the executable

# Find the command to run the project
# Assumes that it is already in the project directory
def find_proj_info(lang_type: Optional[str]) -> ProjInfo:
    # TODO: Add more languages
    langs = {
        'Cargo.toml': rust_proj_info()
    }
    if lang_type is not None:
        return langs.get(lang_type) if langs.get(lang_type) is not None else ProjInfo(build_command = None, proj_name = None, execut_command = None)
    for file, info in langs.items():
        if fexists(file):
            return info
    return ProjInfo(build_command = None, proj_name = None, execut_command = None)

def rust_proj_info() -> ProjInfo:
    build_command = 'cargo build --release'
    toml_contents = None
    with open('Cargo.toml', 'r') as f:
        toml_contents = f.read()
    result = re.search("^name = \\\"(.*)\\\"", toml_contents)
    if result is None:
        return ProjInfo(build_command = None, proj_name = None, execut_command = None)
    proj_name = result.group(1)
    execut_command = "target/release/" + proj_name
    return ProjInfo(build_command = build_command, proj_name = proj_name, execut_command = execut_command)

c = zerorpc.Client()
c.connect("tcp://127.0.0.1:5999")
# c.run_all_progs()
c.finish(3)
sys.exit(0)
