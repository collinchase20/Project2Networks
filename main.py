import argparse
from interpreter import FTPInterpreter


def main():
    # Set up an argument parser for the terminal
    parser = argparse.ArgumentParser()


    # Add arguments
    parser.add_argument('command', type=str)
    parser.add_argument("url", type=str)

    args = parser.parse_args()
    interpreter = FTPInterpreter()

    if (args.command == None or args.url == None):
        return Exception ("You need to provide at least a command and FTP URL")

    #Get the Username and Password from the FTP URL
    initialString = args.url.split("@")[0]
    password = initialString.split(":")[2]
    process = initialString.split(":")[1]
    username = process.split("//")[1]

    #Get the Directory Provided
    initialString2 = args.url.split("@")[1]
    directoryString = ""
    urlSplit = initialString2.split("/")
    for i in range(len(urlSplit)):
        if i == 0:
            continue
        else:
            directoryString += "/"
            directoryString += urlSplit[i]



    print("The directory string is:" + directoryString)



    if (args.command == "ls"):
        print("Starting list process")
        initialConnect(interpreter, username, password)
        interpreter.doList(directoryString)
        interpreter.doDisconnect()
    elif (args.command == "mkdir"):
        print("Starting make directory process")
        initialConnect(interpreter, username, password)
        interpreter.doMkdir(directoryString)
        interpreter.doDisconnect()
    elif (args.command == "rm"):
        print("Starting rm process")
        initialConnect(interpreter, username, password)
        interpreter.doRm(directoryString)
        interpreter.doDisconnect()
    elif (args.command == "rmdir"):
        print("Starting remove directory process")
        initialConnect(interpreter, username, password)
        interpreter.doRmdir(directoryString)
        interpreter.doDisconnect()
    else:
        print("Please provide a valid command (ls, mkdir, rmdir, rm")


def initialConnect(interpreter, username, password):
    interpreter.doConnect("networks-teaching-ftp.ccs.neu.edu")
    interpreter.doLogin(username, password)


main()