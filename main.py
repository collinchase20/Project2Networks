import sys
import argparse
from interpreter import FtpInterpreter


def main():
    # Set up an argument parser for the terminal
    parser = argparse.ArgumentParser()


    # Add arguments
    parser.add_argument('-ls', action='store_true')
    parser.add_argument('-mkdir', action='store_true')
    parser.add_argument('-rm', action='store_true')
    parser.add_argument('-rmdir', action='store_true')
    parser.add_argument("url")

    args = parser.parse_args()

    ftps_interpreter = FtpInterpreter()

    ftps_interpreter.do_connect("networks-teaching-ftp.ccs.neu.edu")

    if (not args.ls and not args.mkdir and not args.rm and not args.rmdir):
        print("Please provide one valid FTP operation (ls, mkdir, rm, rmdir)")
    elif (args.ls is not None):
        ftps_interpreter.do_list(args.url)
    elif (args.mkdir is not None):
        ftps_interpreter.do_mkdir(args.url)
    elif (args.rm is not None):
        ftps_interpreter.do_rm(args.url)
    elif (args.rmdir is not None):
        ftps_interpreter.do_rmdir(args.url)
    else:
        print("Should Not Come Here")



main()