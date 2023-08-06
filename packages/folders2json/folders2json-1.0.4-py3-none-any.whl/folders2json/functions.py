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
    parser.add_argument('-w', '--windows', dest='windows', action='store_true', default=False, help='If you are using windows adds extra slash for file path.' )
    args = parser.parse_args()

    return args


def GetFullPathFiles(rootpath):
    """Get all the files into a list."""
    fullpathfiles = list()
    for root, _, filenames in os.walk(rootpath):
        rel_dir = os.path.relpath(root, rootpath)
        for filename in filenames:
            fullpathfiles.append(os.path.join(rel_dir, filename))
    return fullpathfiles


def GetDevices(pathlist, rootpath, win):
    """Get unique device ids as keys in default dictionary."""
    deviceiddict = defaultdict(list)
    abs_dir = os.path.abspath(rootpath)
    for fullpath in pathlist:
        pathchunks = Path(fullpath).parts
        if len(pathchunks) > 3:
            absfull = os.path.join(abs_dir, fullpath)
            if win:
                absfullfinal = f"file://{absfull}"
            else:
                absfullfinal = f"file:/{absfull}"
            deviceiddict[pathchunks[3]].append(absfullfinal)
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
