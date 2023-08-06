from .functions import GetFullPathFiles, GetDevices, GenerateJson, prep


__version__ = "1.0.4"


def main():
    args = prep()  # get rootpath
    fullnamefiles = GetFullPathFiles(args.rootpath)  # get relative path files
    devices = GetDevices(fullnamefiles, args.rootpath, args.windows)  # get devices for json prep
    GenerateJson(devices)  # generate json file for each


if __name__ == "__main__":
    main()
