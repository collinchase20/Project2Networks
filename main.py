import sys
import argparse
from interpreter import FtpInterpreter


def main():
    # Set up an argument parser for the terminal
    parser = argparse.ArgumentParser()


    # Add arguments
    parser.add_argument('-ls', type=str, required=False)
    parser.add_argument('-mkdir', type=str, required=False)
    parser.add_argument('-rm', type=str, required=False)
    parser.add_argument('-rmdir', type=str, required=False)
    parser.add_argument("url", type=str, required=True)
    parser.add_argument("url2", type=str, required=False)

    args = parser.parse_args()

    ftps_interpreter = FtpInterpreter()

    ftps_interpreter.do_connect("networks-teaching-ftp.ccs.neu.edu")

    if not len(sys.argv) > 1:
        print("Please pass an argument to the program." + "\n")
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