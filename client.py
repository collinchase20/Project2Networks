import socket
import os

#FTP CLient Class which holds methods to perform the various commands required
class FTPClient():

    #Initialize FTPClient class with an instance of a control socket and a datasocket
    #Both set to None until initialized
    def __init__(self):
        self.controlSocket = None
        self.dataSocket = None


    #Send command method to send command to FTP server
    def sendCommand(self, command, arg=None):
        if arg is not None:
            #print("SENDING COMMAND: " + command)
            command = '{} {}'.format(command, arg)
            newcommand = '{}\r\n'.format(command)
            finalcommand = str.encode(newcommand)
        else:
            #print("SENDING COMMAND: " + command)
            newcommand = '{}\r\n'.format(command)
            finalcommand = str.encode(newcommand)
        try:
            self.controlSocket.sendall(finalcommand)
        except Exception:
            print ("Error Sending Command: " + command)
            exit()

    #Receieve command data method to return the response from the FTP server
    def recieveCommandData(self):
        data = self.controlSocket.recv(1024)
        return data

    #OpenDataChannel method to send the required commands before uploading or downloading any data
    #Connects a data socket at the end with the IP and Port reieved from the FTP server for the data socket
    def openDataChannel(self):
        #Set the TYPE, MODE and STRU before attempting to download or upload any data
        self.sendCommand("TYPE", "I")
        response = self.recieveCommandData()
        #print(response)
        self.sendCommand("MODE", "S")
        response = self.recieveCommandData()
        #print(response)
        self.sendCommand("STRU", "F")
        response = self.recieveCommandData()
        #print(response)
        #Ask the FTP server to open a data channel
        self.sendCommand("PASV")
        dataChannelResponse = self.recieveCommandData()
        print(dataChannelResponse)
        #Connect a data socket with the response from the FTP server
        self.connectDataSocket(dataChannelResponse)


    #ConnectDataSocket method which connects the data socket with the IP and Port provided from the FTP server
    #Param: Response - the response from the FTP server when asking to open a data socket
    def connectDataSocket(self, response):
        response = response.decode()
        #Get the ip address and port from the response
        partialNumbers = response.split(" ")[4]
        numbers = partialNumbers.split(".")[0]
        y = numbers.replace("(", "")
        x = y.replace(")", "")
        listOfNumbers = x.split(",")
        ip = ""
        bit1 = 0
        bit2 = 0
        for i in range(len(listOfNumbers)):
            if i <= 2:
                ip += listOfNumbers[i]
                ip += "."
            elif i == 3:
                ip += listOfNumbers[i]
            elif i == 4:
                bit1 += int(listOfNumbers[4])
            elif i == 5:
                bit2 += int(listOfNumbers[5])
        port = (bit1 << 8) + bit2
        #Initialize a data socket with the IP and port from the response
        self.dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.dataSocket.connect((ip, port))

    #readFromDataChannel method to recieve the data from the opened dataChannel
    #Param: File: where we are writing the data to. If not provided we are printing the data
    def readFromDataChannel(self, file=None):
        data = ""
        someData = self.dataSocket.recv(4096)
        try:
            decodedData = someData.decode()
        except:
            print("Cant decode certain byte from the file. File could be corupt.")
            exit()
        data += decodedData
        while decodedData != "":
            someData = self.dataSocket.recv(4096)
            decodedData = someData.decode()
            data += decodedData
        #If file not provided we are in LS command and printing directory
        if file == None:
            print(data)
        #Else we are writing the data to the file provided
        else:
            with open(file, 'w') as openedFile:
                return openedFile.write(data)

    #writeToDataChannel method to send data to our opened data socket.
    #Param: File: the file in which we are reading the data and sending to the data channel
    def writeToDataChannel(self, file):
        with open(file, 'r') as openedFile:
            data = openedFile.read(4096)
            dataencoded = data.encode()
            while data:
                self.dataSocket.send(dataencoded)
                data = openedFile.read(4096)
                dataencoded = data.encode()

    #closeDataChannel method to close the data socket after it has been used. Should be closed after each command
    #that requires use of the data socket.
    def closeDataChannel(self):
        self.dataSocket.close()

    #MV method which performs the move operation to move a file from one place to another
    def mv(self, directory, file, isFTPFirst):
        #We first use the copy function to copy the file to where it is going
        self.cp(directory, file, isFTPFirst)
        #We then use the delete function to delete the file from where it came from
        #or we remove the file from the operating system with the os library
        if isFTPFirst:
            self.rm(directory)
        else:
            os.remove(file)

    #CP method which copies a file from one place to another
    def cp(self, directory, file, isFTPFirst):
        #If the FTP URL was the first parameter we are copying the file there to local
        if isFTPFirst:
            self.openDataChannel()
            self.sendCommand("RETR", directory)
            data = self.readFromDataChannel(file)
            print(data)
        #Else if the FTP URL was not first we are copying a local file to ftp
        else:
            self.openDataChannel()
            self.sendCommand("STOR", directory)
            try:
                self.writeToDataChannel(file)
            except Exception:
                print("There was a problem trying to open and find the file or write to data channel " + file)
                exit()
        #Close the data channel when we are done with it
        self.closeDataChannel()


    #List method which writes the directory listing of the directory provided to the terminal
    def list(self, directory=None):
        self.openDataChannel()
        #If file name is None we are listing the root directory
        if directory is not None:
            self.sendCommand("LIST", directory)
        else:
            self.sendCommand("LIST")
        data = self.recieveCommandData()
        print(data)
        self.readFromDataChannel()
        #Close the data channel now that we are done with it
        self.closeDataChannel()

    #RM method which removes a file at the specified location provided by the directory command
    def rm(self, directory):
        self.sendCommand("DELE", directory)
        data = self.recieveCommandData()
        print(data)
        if (str.encode("550") in data):
            print ("Cant remove the file. Check if the path you provided is to an actual file and is not a directory.")
            exit()

    #MKDIR command which makes a directory on the FTP server at the provided location
    def mkdir(self, directory):
        self.sendCommand("MKD", directory)
        data = self.recieveCommandData()
        print(data)
        if (str.encode("550") in data):
            print ("Cant make the directory. Check if the path you specified to make a directory is correct and that the directory does "
                    "not already exist. Note: you cannot make multiple directories at the same time.")
            exit()

    #RMDIR command which removes a directory from the FTP server at the provided location
    def rmdir(self, directory):
        self.sendCommand("RMD", directory)
        data = self.recieveCommandData()
        print(data)
        if (str.encode("550") in data):
            print ("Cant remove directory. Check the path is correct and that the directory you are trying to "
                    "remove actually exists. Also you cannot remove directories that have files in them.")
            exit()

    #Connect method which connects our control socket to the FTP server with the provided host and port
    def connect(self, host, port):
        try:
            self.controlSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.controlSocket.connect((host, port))
        except Exception:
            print ("Error trying to connect to host. Check the Host or the Port.")
            exit()
        data = self.recieveCommandData()
        print(data)


    #Disconnect method which disconnects the program from the FTP server
    def disconnect(self):
        self.sendCommand("QUIT")
        data = self.recieveCommandData()
        print(data)

    #Login method which logs a user into the FTP server with the specified username and password as paramters
    def login(self, user, password):
        self.sendCommand("USER", user)
        self.recieveCommandData()
        self.sendCommand("PASS", password)
        data = self.recieveCommandData()
        print(data)
        if (str.encode("530") in data):
            print ("Error with the username or the password.")
            exit()
