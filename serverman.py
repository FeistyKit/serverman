#!/usr/bin/env python

import zerorpc, os, re, pathlib, sys, argparse, yaml
from typing import Optional
from dataclasses import dataclass

HOME_DIR = os.environ['HOME']

# If file exists
def fexists(path: str) -> bool:
    return pathlib.Path(path).is_file()

# if dir exists
def dexists(path: str) -> bool:
    return pathlib.Path(path).is_dir()




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
        'rust': 'Cargo.toml'
    }
    lang_files = {
        'Cargo.toml': rust_proj_info
    }
    if lang_type is not None:
        a = langs.get(lang_type)
        if a is None:
            return ProjInfo(build_command = None, proj_name = None, execut_command = None)
        b = lang_files.get(a)
        return b() if b is not None else ProjInfo(build_command = None, proj_name = None, execut_command = None)
    for file, info in lang_files.items():
        if fexists(file):
            return info()
    return ProjInfo(build_command = None, proj_name = None, execut_command = None)

def rust_proj_info() -> ProjInfo:
    build_command = 'cargo build --release'
    toml_contents = None
    with open('Cargo.toml', 'r') as f:
        toml_contents = f.read()
    reg = re.compile(r"^name = \"(.*)\"", re.MULTILINE)
    result = reg.search(toml_contents)
    if result is None:
        return ProjInfo(build_command = build_command, proj_name = None, execut_command = None)
    proj_name = result.group(1)
    execut_command = "target/release/" + proj_name
    return ProjInfo(build_command = build_command, proj_name = proj_name, execut_command = execut_command)

# detect the type of project and automatically make a config file for it
# TODO: customizable default yaml path
def generate_config_file(info: ProjInfo):
    with open(".serverman.yml", "w") as f:
        f.write("# this file was generated automatically by serverman. <https://www.github.com/FeistyKit/serverman> Modify it as you wish!\n")
        info_object = {
            'proj_name': info.proj_name,
            'exe-path': info.execut_command,
            'build_command': info.build_command
        }
        f.write(yaml.dump(info_object))
        print(f"Successfully made config file for {info.proj_name}!")

# TODOOO: Find servermanserver.py and start it
def start(args):
    pass

def init(args):
    print("Trying to find project info...")
    try:
        os.chdir(args.DIR)
    except:
        print(f"Could not open directory {args.DIR}! Cancelling!", file=sys.stderr)
    info = find_proj_info(args.lang)
    if args.build_command is not None:
        info.build_command = args.build_command
    if args.exe_path is not None:
        info.execut_command = args.exe_path
    if info.build_command is None:
        print("Could not automatically make build command.")
        info.build_command = input("Please input it here:")
    if info.execut_command is None:
        print("Could not automatically find executable path.")
        info.execut_command = input("Please input it here:")
    if info.proj_name is None:
        print("Could not automatically find project name.")
        info.proj_name = input("Please input it here:")
    generate_config_file(info)

parser = argparse.ArgumentParser()
subs = parser.add_subparsers()

init_parser = subs.add_parser('init', help="Attempt to automatically generate a config file for the project.")
init_parser.add_argument("DIR", type=str)
init_parser.add_argument("--lang", "-l", type=str, help="The language that the project is written in.")
init_parser.add_argument("--build_command", type=str, help="the bash command to build the project")
init_parser.add_argument("--exe-path", type=str, help="The path to the executable")
init_parser.set_defaults(func=init)

args = parser.parse_args()
args.func(args)
