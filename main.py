import argparse
from client import FTPClient

#Main method to run the protocol
def main():
    # Set up an argument parser for the terminal
    parser = argparse.ArgumentParser()

    # Add arguments
    parser.add_argument('command', type=str)
    parser.add_argument(dest='params', metavar='params', nargs='*', type=str)
    args = parser.parse_args()

    #If no command is provided throw an exception
    if (args.command == None):
        print ("You need to provide at least a command and FTP URL")
        exit()
    #If no additional params are provided or more than 2 params are provided throw an exception
    if len(args.params) > 2 or len(args.params) < 1:
        print ("Unsupported number of arguments.")
        exit()

    #Initialize FTPClient
    client = FTPClient()

    #Initialize the fields for the command
    host = ""
    port = 21
    username = ""
    password = ""
    file = ""
    directory = ""
    isFTPFirst = False

    if (len(args.params) == 2):
        if (args.params[0].startswith("ftp://")):
            isFTPFirst = True
            username = getUsername(args.params[0])
            password = getPassword(args.params[0])
            host = getHost(args.params[0])
            port = getPort(args.params[0])
            file = args.params[1]
            directory = getDirectory(args.params[0])
        elif (args.params[1].startswith("ftp://")):
            username = getUsername(args.params[1])
            password = getPassword(args.params[1])
            host = getHost(args.params[1])
            port = getPort(args.params[1])
            file = args.params[0]
            directory = getDirectory(args.params[1])
        else:
            print ("If you are going to provide two parameters one of them has to be an ftp server")
            return
    else:
        username = getUsername(args.params[0])
        password = getPassword(args.params[0])
        directory = getDirectory(args.params[0])
        host = getHost(args.params[0])
        port = getPort(args.params[0])

    #Check the command provided from input. If the command is not valid throw an exception.
    if (args.command == "ls"):
        initialConnect(client, host, port, username, password)
        client.list(directory)
        client.disconnect()
    elif (args.command == "mkdir"):
        initialConnect(client, host, port, username, password)
        client.mkdir(directory)
        client.disconnect()
    elif (args.command == "rm"):
        initialConnect(client, host, port, username, password)
        client.rm(directory)
        client.disconnect()
    elif (args.command == "rmdir"):
        initialConnect(client, host, port, username, password)
        client.rmdir(directory)
        client.disconnect()
    elif (args.command == "cp"):
        initialConnect(client, host, port, username, password)
        client.cp(directory, file, isFTPFirst)
        client.disconnect()
    elif (args.command == "mv"):
        initialConnect(client, host, port, username, password)
        client.mv(directory, file, isFTPFirst)
        client.disconnect()
    else:
        print ("Please provide a valid command as the first argument (ls, mkdir, rmdir, rm, cp, or mv")
        exit()



#InitialConnect method to connect to our FTP server and potentially login with a user and password
def initialConnect(client, host, port, username="", password=""):
    client.connect(host, port)
    if username is not "" and password is not "":
        client.login(username, password)


#Get the directory from the specified FTP url
def getDirectory(string):
    if "@" not in string:
        initialString = string.split("/")
        directory = ""
        for i in range(len(initialString)):
            if i == 0 or i == 1 or i == 2:
                continue
            else:
                directory += "/"
                directory += initialString[i]
        return directory
    else:
        initialString2 = string.split("@")[1]
        directory = ""
        urlSplit = initialString2.split("/")
        for i in range(len(urlSplit)):
            if i == 0:
                continue
            else:
                directory += "/"
                directory += urlSplit[i]
        return directory

#Get the username from the FTP url
def getUsername(string):
    if "@" not in string:
        return "anonymous"
    else:
        initialString = string.split("@")[0]
        process = initialString.split(":")[1]
        username = process.split("//")[1]
        return username

#Get the password from the FTP url
def getPassword(string):
    if "@" not in string:
        return ""
    else:
        initialString = string.split("@")[0]
        password = initialString.split(":")[2]
        return password

#Get the Host from the FTP url
def getHost(string):
    ftp = "ftp://"
    if "@" not in string:
        string = string[string.startswith(ftp) and len(ftp):]
        newstring = string.split("/")[0]
        if ":" in newstring:
            return newstring.split(":")[0]
        else:
            return newstring
    else:
        if ":" not in string:
            initialString = string.split("@")[1]
            returnString = initialString.split("/")[0]
            return returnString
        else:
            initialString = string.split("@")[1]
            returnString = initialString.split("/")[0]
            finalString = returnString.split(":")[0]
            return finalString

#Get the port from the FTP url
def getPort(string):
    ftp = "ftp://"
    if "@" not in string:
        string = string[string.startswith(ftp) and len(ftp):]
        newstring = string.split("/")[0]
        if ":" not in newstring:
            return 21
        else:
            return newstring.split(":")[1]
    else:
        initialString = string.split("@")[1]
        if ":" not in initialString:
            return 21
        else:
            returnString = initialString.split(":")[1]
            finalString = returnString.split("/")[0]
            return int(finalString)

main()