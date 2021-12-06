#!/usr/bin/env python

# The server of the program

import zerorpc, argparse, os, json, pathlib, logging, yaml, shlex, subprocess
from dataclasses import dataclass

# PYTHON DEPENDENCIES: zerorpc, pyyaml
# DEPENDS UPON: tar, gzip

parser = argparse.ArgumentParser(description="The server part of serverman. THIS PROGRAM IS NOT MEANT FOR HUMAN USE: PLEASE USE THE OTHER PROGRAM IN THE REPO.")
parser.add_argument('dir', type=str, nargs=1)
parser.add_argument('--progs-to-run', type=str, nargs="*", default=[])
parser.add_argument('--progs-to-not-run', type=str, nargs="*", default=[])
parser.add_argument('--no-auto-configs', default=False, const=True, action='store_const')
args = parser.parse_args()

os.chdir(args.dir)

# If file exists
def fexists(path: str) -> bool:
    return pathlib.Path(path).is_file()

# if dire exists
def dexists(path: str) -> bool:
    return pathlib.Path(path).is_dir()

class ServerMan():
    def __init__(self):
        pathlib.Path("data.json").touch()
        with open("data.json", "r") as f:
            try:
                self.prog_info = json.loads(f.read())
                logging.info("Read %s items from data.json!", len(self.prog_info))
            except Exception:
                logging.error("Could not parse `data.json`! Continuing with empty program list...")
        self.progs: list[tuple[str, subprocess.Popen]] = []

    # Run all programs
    # TODOO: run_all_progs
    def run_all_progs(self):
        for name, path in self.prog_info.items():
            self.run_prog(name, path)

    # run the programs specified to be run
    # TODOO: run only some programs
    def run_only_progs(self, to_run):
        pass

    # Run all of the programs except the excluded ones
    # TODOO: run programs excluding
    def run_progs_excluding(self, to_not_run):
        pass

    def run_prog(self, name: str, path: str):
        if not dexists(path):
            logging.error("Could not open directory for `%s`! Perhaps it was deleted?", name)
            return
        os.chdir(path)
        if not fexists(".serverman.yml"):
            logging.error("Could not find .serverman.yml for project `%s`", name)
            return
        content = None
        with open('.serverman.yml', 'r') as f:
            try:
                content = yaml.safe_load(f.read())
            except Exception:
                logging.error("Could not parse .serverman.yml for program `%s`", name)
                return
        command = shlex.split(content['execut_command'])
        with subprocess.Popen(command) as p:
            self.progs.append((name, p))




# Prepare the logging file
def prepare_logging():
    if fexists("latest.log"):
        tim = os.path.getmtime("latest.log")
        os.system(["tar", "-cvf", f"{tim}.tar.gz", "latest.log"])
    assert not fexists("latest.log"), "Logfile should not exist!"
    logging.basicConfig(filename='latest.log', encoding='utf-8', level=logging.DEBUG)
