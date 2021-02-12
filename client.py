import socket

class FTPClient():

    PORT = 21
    SOCKET_TIMEOUT_SECONDS = 5
    SOCKET_RCV_BYTES = 4096

    USER_COMMAND = 'USER'
    PASS_COMMAND = 'PASS'
    TYPE_COMMAND = 'TYPE'
    MODE_COMMAND = 'MODE'
    STRU_COMMAND = "STRU"
    LIST_COMMAND = 'LIST'
    DELE_COMMAND = 'DELE'
    MKD_COMMAND = 'MKD'
    RMD_COMMAND = 'RMD'
    STOR_COMMAND = 'STOR'
    RETR_COMMAND = 'RETR'
    QUIT_COMMAND = 'QUIT'
    PASV_COMMAND = 'PASV'
    EPRT_COMMAND = 'ERPT'

    STATUS_230 = str.encode('230')
    STATUS_550 = str.encode('550')
    STATUS_530 = str.encode('530')

    def __init__(self):
        self.resetSockets()


    def resetSockets(self):
        self.resetControlSocket()
        self.resetDataSocket()
        self.host = None
        self.user = None

    def resetControlSocket(self):
        if getattr(self, 'host', None) is not None:
            self.controlSocket.close()
        self.controlSocket = socket.socket()
        self.controlSocket.settimeout(FTPClient.SOCKET_TIMEOUT_SECONDS)

    def resetDataSocket(self):
        if getattr(self, '_data_socket_listening', False):
            self.dataSocket.close()
        self.dataSocket = socket.socket()
        self._data_socket_listening = False

    def sendCommand(self, command, *args):
        print("preparing to send command data")
        for a in args:
            command = '{} {}'.format(command, a)
            newcommand = '{}\r\n'.format(command)
            finalcommand = str.encode(newcommand)
        try:
            self.controlSocket.sendall(finalcommand)
        except socket.timeout as e:
            print("error sending command")
            raise Exception (e)

    def sendCommandNoArguments(self, command):
        newcommand = '{}\r\n'.format(command)
        finalcommand = str.encode(newcommand)
        try:
            self.controlSocket.sendall(finalcommand)
        except socket.timeout as e:
            raise Exception (e)


    def _receive_command_data(self):
        print("recieving command data")
        data = self.controlSocket.recv(FTPClient.SOCKET_RCV_BYTES)
        return data

    def checkIfConnected(self):
        if self.host is None:
            print("You are not connected")
            raise Exception("You are not connected to a FTP server.")

    def checkIfAuthenticated(self):
        if self.user is None:
            print("You are not authenticated")
            raise Exception("You are not authenticated for the FTP server.")

    def openDataChannel(self):
        self.sendCommandNoArguments(FTPClient.PASV_COMMAND)
        dataChannelResponse = self._receive_command_data()
        print(dataChannelResponse)
        self.connectDataTCPSocket(dataChannelResponse)

    def connectDataTCPSocket(self, response):
        response = response.decode()
        print(response)
        partialNumbers = response.split(" ")[4]
        numbers = partialNumbers.split(".")[0]
        print(numbers)

        self.dataSocket = socket.socket()
        #self.dataSocket.connect(ip, port)

    def _open_data_socket(self):
        self._data_address, self._data_port = \
            self.controlSocket.getsockname()
        self._data_port = self._data_port + 1
        self.dataSocket.bind(('', self._data_port))
        self.dataSocket.listen(1)
        self._data_socket_listening = True

    def _open_data_connection(self):
        if not self._data_socket_listening:
            self._open_data_socket()
        self.sendCommand(FTPClient.EPRT_COMMAND, '|1|{}|{}|'
                           .format(self._data_address, self._data_port))
        self._data_connection, address = self.dataSocket.accept()
        data = self._receive_command_data()
        return data

    def _read_from_data_connection(self):
        total_data = ''
        while True:
            data = self._data_connection.recv(FTPClient.SOCKET_RCV_BYTES)
            total_data = total_data + data
            if not data:
                break
        self._data_connection.close()
        return total_data

    def _write_to_data_connection(self, content):
        self._data_connection.sendall(content)
        self._data_connection.close()

    def connect(self, host):

        if self.host is not None:
            self.resetSockets()

        try:
            self.controlSocket.connect((host, FTPClient.PORT))
            self.host = host
        except socket.error as e:
            self.resetSockets()
            raise Exception(e)

        return self._receive_command_data()

    def disconnect(self):
        self.checkIfConnected()

        self.sendCommandNoArguments(FTPClient.QUIT_COMMAND)
        data = self._receive_command_data()
        self.resetSockets()

        return data

    def login(self, user, password):

        self.checkIfConnected()

        self.sendCommand(FTPClient.USER_COMMAND, user)
        self._receive_command_data()

        self.sendCommand(FTPClient.PASS_COMMAND, password)
        data = self._receive_command_data()

        if data.startswith(FTPClient.STATUS_230):
            self.user = user
        elif data.startswith(FTPClient.STATUS_530):
            self.user = None

        return data


    def list(self, filename=None):

        self.checkIfConnected()
        self.checkIfAuthenticated()
        self.openDataChannel()

        data = self._open_data_connection()

        if filename is not None:
            self.sendCommand(FTPClient.LIST_COMMAND, filename)
        else:
            self.sendCommand(FTPClient.LIST_COMMAND)

        list_data = self._receive_command_data()
        data = data + list_data

        if not list_data.startswith(FTPClient.STATUS_550):
            data = data + self._read_from_data_connection()
            data = data + self._receive_command_data()

        return data


    def mkdir(self, directory):

        print("at the client trying to make directory")
        self.checkIfConnected()
        self.checkIfAuthenticated()
        print("here trying to make directory")
        self.sendCommand(FTPClient.MKD_COMMAND, directory)
        data = self._receive_command_data()

        return data

    def rm(self, filename):

        self.checkIfConnected()
        self.checkIfAuthenticated()

        self.sendCommand(FTPClient.DELE_COMMAND, filename)
        data = self._receive_command_data()

        return data

    def rmdir(self, directory):

        self.checkIfConnected()
        self.checkIfAuthenticated()

        self.sendCommand(FTPClient.RMD_COMMAND, directory)
        data = self._receive_command_data()

        return data
