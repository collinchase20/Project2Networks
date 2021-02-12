from client import FTPClient


class FTPInterpreter():
    """
    FTP client command line utility.
    """
    def __init__(self):
        self.ftpClient = FTPClient()


    def doConnect(self, host):
        response = self.ftpClient.connect(host)
        print("This is the connect response")
        print(response)

    def doDisconnect(self):
        response = self.ftpClient.disconnect()
        print("This is the disconnect response")
        print(response)

    def doLogin(self, user, password):
        response = self.ftpClient.login(user, password)
        print("This is the login response")
        print(response)


    def doList(self, filename):
        response = self.ftpClient.list(filename)
        print("This is the list response")
        print(response)


    def doMkdir(self, directory):
        print("starting to make directory")
        response = self.ftpClient.mkdir(directory)
        print("This is the make directory response")
        print(response)

    def doRm(self, filename):
        response = self.ftpClient.rm(filename)
        print("This is the remove file response")
        print (response)

    def doRmdir(self, directory):
        response = self.ftpClient.rmdir(directory)
        print("This is the remove directory response")
        print (response)