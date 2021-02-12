import sys
import argparse
from interpreter import FtpInterpreter


def main():
    # Set up an argument parser for the terminal
    parser = argparse.ArgumentParser()


    # Add arguments
    parser.add_argument('command')
    #parser.add_argument('-mkdir', action='store_true')
    #parser.add_argument('-rm', action='store_true')
    #parser.add_argument('-rmdir', action='store_true')
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


    if (args.command != "mkdir" or args.command != "ls" or args.command != "rm" or args.command != "rmdir"):
        print("Please provide one valid FTP operation (ls, mkdir, rm, rmdir)")
    elif (args.command == "ls"):
        print("Starting list process")
        initialConnect(interpreter, username, password)
        interpreter.do_list("Test")
        interpreter.do_disconnect()
    elif (args.command == "mkdir"):
        print("Starting make directory process")
        initialConnect(interpreter, username, password)
        interpreter.do_mkdir("/MyMadeDirectory")
        interpreter.do_disconnect()
    elif (args.command == "rm"):
        print("Starting rm process")
        initialConnect(interpreter, username, password)
        #interpreter.do_rm(args.url)
        interpreter.do_disconnect()
    elif (args.command == "rmdir"):
        print("Starting remove directory process")
        initialConnect(interpreter, username, password)
        interpreter.do_rmdir("/Test")
        interpreter.do_disconnect()
    else:
        print("Invalid Command")


def initialConnect(interpreter, username, password):
    interpreter.do_connect("networks-teaching-ftp.ccs.neu.edu")
    interpreter.do_login(username, password)





main()