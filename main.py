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
    interpreter = FtpInterpreter()

    if (not args.ls and not args.mkdir and not args.rm and not args.rmdir):
        print("Please provide one valid FTP operation (ls, mkdir, rm, rmdir)")
    elif (args.ls is not None):
        interpreter = initialConnect(interpreter)
        interpreter.do_list(args.url)
        logoutAndDisconnect(interpreter)
    elif (args.mkdir is not None):
        interpreter = initialConnect(interpreter)
        interpreter.do_mkdir(args.url)
        return Exception(args.url)
        logoutAndDisconnect(interpreter)
    elif (args.rm is not None):
        interpreter = initialConnect(interpreter)
        interpreter.do_rm(args.url)
        logoutAndDisconnect(interpreter)
    elif (args.rmdir is not None):
        interpreter = initialConnect(interpreter)
        interpreter.do_rmdir(args.url)
        logoutAndDisconnect(interpreter)
    else:
        print("Should Not Come Here")


def initialConnect(interpreter):
    interpreter.do_connect("networks-teaching-ftp.ccs.neu.edu")
    interpreter.do_login()
    return interpreter

def logoutAndDisconnect(interpreter):
    interpreter.do_logout()
    interpreter.do_disconnect()





main()