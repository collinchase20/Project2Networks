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

    #Get the username and password from ftp url
    initialString = args.url.split("@")[0]
    password = initialString.split(":")[2]
    process = initialString.split(":")[1]
    username = process.split("//")[1]

    #Get the url
    initalString2 = args.url.split("@")[1]


    if (not args.ls and not args.mkdir and not args.rm and not args.rmdir):
        print("Please provide one valid FTP operation (ls, mkdir, rm, rmdir)")
    elif (args.ls is not None):
        print("Starting list process")
        initialConnect(interpreter, username, password)
        #interpreter.do_list("Test")
        interpreter.do_disconnect()
    elif (args.mkdir is not None):
        print("Starting make directory process")
        initialConnect(interpreter, username, password)
        interpreter.do_mkdir("/MyMadeDirectory")
        interpreter.do_disconnect()
    elif (args.rm is not None):
        print("Starting rm process")
        initialConnect(interpreter, username, password)
        #interpreter.do_rm(args.url)
        interpreter.do_disconnect()
    elif (args.rmdir is not None):
        print("Starting remove directory process")
        initialConnect(interpreter, username, password)
        interpreter.do_rmdir("/Test")
        interpreter.do_disconnect()
    else:
        print("Should Not Come Here")


def initialConnect(interpreter, username, password):
    interpreter.do_connect("networks-teaching-ftp.ccs.neu.edu")
    interpreter.do_login(username, password)





main()