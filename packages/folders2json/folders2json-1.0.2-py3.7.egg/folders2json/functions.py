"""Functions for folders2json."""
import os
from pathlib import Path
import json
from collections import defaultdict
import argparse

currentdir = os.getcwd()


def prep():
    """Get all the argparse stuff setup."""
    parser = argparse.ArgumentParser(description='simple generate json\
                                     for folder format')
    parser.add_argument('-r', '--root', dest='rootpath',
                        help='Set the root path', default=currentdir,
                        required=False)
    args = parser.parse_args()
    return args


def GetFullPathFiles(rootpath):
    """Get all the files into a list."""
    fullpathfiles = list()
    for root, _, filenames in os.walk(rootpath):
        abs_dir = os.path.abspath(root)
        for filename in filenames:
            fullness = f"file:/{os.path.join(abs_dir, filename)}"
            fullpathfiles.append(fullness)
    print(fullpathfiles)
    return fullpathfiles


def GetDevices(pathlist):
    """Get unique device ids as keys in default dictionary."""
    deviceiddict = defaultdict(list)
    for fullpath in pathlist:
        pathchunks = Path(fullpath).parts
        if len(pathchunks) > 3:
            deviceiddict[pathchunks[3]].append(fullpath)
    return deviceiddict


def GenerateJson(deviceiddict):
    """For each deviceid key, generate json."""
    finaldict = dict()
    for key, value in deviceiddict.items():
        finaldict["urls"] = value
        partsofpath = Path(value[0]).parts
        if len(partsofpath) > 3:
            finaldict["metadata"] = {
                "objective": partsofpath[0],
                "batch": partsofpath[1],
                "device": key
            }
        finaldict["params"] = {}
        with open(f"{key}.json", "w+") as f:
            f.write(json.dumps(finaldict))
