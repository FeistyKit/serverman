#!/usr/bin/env python

# The server of the program

import zerorpc, argparse, os, json, pathlib, logging
from typing import Optional

# PYTHON DEPENDENCIES: zerorpc, pyyaml
# DEPENDS UPON: zip

parser = argparse.ArgumentParser(description="The server part of serverman. THIS PROGRAM IS NOT MEANT FOR HUMAN USE: PLEASE USE THE OTHER PROGRAM IN THE REPO.")
parser.add_argument('dir', type=str, nargs=1)
parser.add_argument('--progs-to-run', type=str, nargs="*", default=[])
parser.add_argument('--progs-to-not-run', type=str, nargs="*", default=[])
parser.add_argument('--no-auto-configs', type=bool, default=False, const=True, action='store_const')
args = parser.parse_args()

os.chdir(args.dir)

# If file exists
def fexists(path: str) -> bool:
    return pathlib.Path(path).is_file()

# if dire exists
def dexists(path: str) -> bool:
    return pathlib.Path(path).is_dir()

class ServerMan(object):
    def __init__(self):
        pathlib.Path("data.json").touch()
        with open("data.json", "r") as f:
            try:
                self.progs = json.loads(f.read())
                logging.info(f"Read {len(self.progs)} items from data.json!")
            except Exception:
                logging.error(f"Could not parse `data.json`! Continuing with empty program list...")

    # Run all programs
    # TODOO: run_all_progs
    def run_all_progs(self, log):
        pass

    # run the programs specified to be run
    # TODOO: run only some programs
    def run_only_progs(self, to_run):
        pass

    # Run all of the programs except the excluded ones
    # TODOO: run programs excluding
    def run_progs_excluding(self, to_not_run):
        pass

def run_prog(name: str, path: str):
    if not dexists(path):
        logging.error(f"Could not open directory for `{name}`! Perhaps it was deleted?")
        return

# detect the type of project and automatically make a config file for it
# TODO: customizable default yaml
def generate_config_file(path: str, lang_type: Optional[str] =None):
    yaml = ""
    with open(path, "w") as f:
        f.write("# this file was generated automatically by serverman. <https://www.github.com/FeistyKit/serverman> Modify it as you wish!")

# Find the command to run the project
# Assumes that it is already in the project directory
def find_build_command(lang_type: Optional[str]) -> Optional[str]:
    if lang_type is not None:
        # TODOOOOOOOO: what to do if given language type for build command generation
        return None
    else:
        # I might clean this up later but I don't really care
        if fexists("Cargo.toml"):
                return "cargo build --release "
        return None

# Prepare the logging file
def prepare_logging():
    if fexists("latest.log"):
        tim = os.path.getmtime("latest.log")
        os.system(["tar", "-cvf", f"{tim}.tar.gz", "latest.log"])
    assert not fexists("latest.log"), "Logfile should not exist!"
    logging.basicConfig(filename='latest.log', encoding='utf-8', level=logging.DEBUG)
