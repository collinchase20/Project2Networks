import sys
import argparse
from interpreter import FtpInterpreter


def main():
    # Set up an argument parser for the terminal
    parser = argparse.ArgumentParser()


    # Add arguments
    parser.add_argument('-ls', '--urlLS', type=str, required=False)
    parser.add_argument('-mkdir', '--urlMKDIR', type=str, required=False)
    parser.add_argument('-rm', '--urlRM', type=str, required=False)
    parser.add_argument('-rmdir', '--urlRMDIR', type=str, required=False)

    args = parser.parse_args()

    ftps_interpreter = FtpInterpreter()

    ftps_interpreter.do_connect("networks-teaching-ftp.ccs.neu.edu")


    if (args.ls):
        ftps_interpreter.do_list(args.urlLS)
    elif (args.mkdir):
        ftps_interpreter.do_mkdir(args.urlMKDIR)
    elif (args.rm):
        ftps_interpreter.do_rm(args.urlRM)
    elif (args.rmdir):
        ftps_interpreter.do_rmdir(args.urlRMDIR)
    else:
        print("Should Not Come Here")



main()