import socket


class FtpClient():
    """
    This class offers a simple interface to interact with an FTP server.
    Attributes:
    host (str): The host to which the client is connected to, if connected,
                None otherwise.
    user (str): The username of the logged in user, if logged in, None
                otherwise.
    """

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

    def __init__(self, debug=False):
        self._debug = debug
        self._reset_sockets()

    def _log(self, info):
        if self._debug:
            print('debug: {}'.format(info))

    def _reset_sockets(self):
        self._reset_command_socket()
        self._reset_data_socket()
        self.host = None
        self.user = None

    def _reset_command_socket(self):
        if getattr(self, 'host', None) is not None:
            self._command_socket.close()
        self._command_socket = socket.socket()
        self._command_socket.settimeout(FtpClient.SOCKET_TIMEOUT_SECONDS)

    def _reset_data_socket(self):
        if getattr(self, '_data_socket_listening', False):
            self._data_socket.close()
        self._data_socket = socket.socket()
        self._data_socket_listening = False

    def _send_command(self, command, *args):
        for a in args:
            command = '{} {}'.format(command, a)
            newcommand = '{}\r\n'.format(command)
            finalcommand = str.encode(newcommand)
        try:
            self._log('sending command - {}'.format(command))
            #self._command_socket.sendall('{}\r\n'.format(command))
            self._command_socket.sendall(finalcommand)
        except socket.timeout as e:
            raise Exception (e)

    def _receive_command_data(self):
        data = self._command_socket.recv(FtpClient.SOCKET_RCV_BYTES)
        self._log('received command data - {}'.format(data))
        return data

    def _check_is_connected(self):
        if self.host is None:
            raise Exception("You are not connected to a FTP server.")

    def _check_is_authenticated(self):
        if self.user is None:
            raise Exception("You are not authenticated for the FTP server.")

    def _open_data_socket(self):
        self._data_address, self._data_port = \
            self._command_socket.getsockname()
        self._data_port = self._data_port + 1
        self._data_socket.bind(('', self._data_port))
        self._data_socket.listen(1)
        self._data_socket_listening = True

    def _open_data_connection(self):
        if not self._data_socket_listening:
            self._open_data_socket()
        self._send_command(FtpClient.EPRT_COMMAND, '|1|{}|{}|'
                           .format(self._data_address, self._data_port))
        self._data_connection, address = self._data_socket.accept()
        self._log('opened data connection on {}'.format(address))
        data = self._receive_command_data()
        return data

    def _read_from_data_connection(self):
        total_data = ''
        while True:
            data = self._data_connection.recv(FtpClient.SOCKET_RCV_BYTES)
            total_data = total_data + data
            if not data:
                break
        self._data_connection.close()
        self._log('received data - {}'.format(total_data))
        return total_data

    def _write_to_data_connection(self, content):
        self._log('sending data - {}'.format(content))
        self._data_connection.sendall(content)
        self._data_connection.close()

    def connect(self, host):
        """
        Connect to an FTP server in the specified host.
        Args:
            host (str): The host to connect to. Falsy values
                        default to `localhost`. (Optional)
        Returns:
            Message from host.
        """
        #host = host or 'localhost'

        if self.host is not None:
            self._reset_sockets()

        try:
            self._log('connecting to {}:{}'.format(host, FtpClient.PORT))
            self._command_socket.connect((host, FtpClient.PORT))
            self.host = host
        except socket.timeout as e:
            self._reset_sockets()
            raise Exception(e)
        except socket.gaierror as e:
            self._reset_sockets()
            raise Exception(e)
        except socket.error as e:
            raise Exception(e)

        return self._receive_command_data()

    def disconnect(self):
        """
        Perform QUIT command (disconnect) on connected host.
        Returns:
            Message from host.
        """
        self._check_is_connected()

        self._send_command(FtpClient.QUIT_COMMAND)
        data = self._receive_command_data()
        self._reset_sockets()

        return data

    def login(self, user, password):
        """
        Login with specified user and password on the connected host.
        Args:
            user (str): The user.
            password (str): The password.
        Returns:
            Message from host.
        """
        self._check_is_connected()

        self._send_command(FtpClient.USER_COMMAND, user)
        self._receive_command_data()

        self._send_command(FtpClient.PASS_COMMAND, password)
        data = self._receive_command_data()

        if data.startswith(FtpClient.STATUS_230):
            self.user = user
        elif data.startswith(FtpClient.STATUS_530):
            self.user = None

        return data


    def list(self, filename=None):
        """
        Perform LIST command on connected host.
        Args:
            filename (str): Name of file or directory to retrieve info
                            for. (Optional)
        Returns:
            Message and data from host.
        """
        self._check_is_connected()
        self._check_is_authenticated()

        data = self._open_data_connection()

        if filename is not None:
            self._send_command(FtpClient.LIST_COMMAND, filename)
        else:
            self._send_command(FtpClient.LIST_COMMAND)

        list_data = self._receive_command_data()
        data = data + list_data

        if not list_data.startswith(FtpClient.STATUS_550):
            data = data + self._read_from_data_connection()
            data = data + self._receive_command_data()

        return data


    def mkdir(self, directory):
        """
        Perform MKD command on connected host.
        Args:
            directory (str): Name of directory to create.
        Returns:
            Message from host.
        """
        self._check_is_connected()
        self._check_is_authenticated()

        self._send_command(FtpClient.MKD_COMMAND, directory)
        data = self._receive_command_data()

        return data

    def rm(self, filename):
        """
        Perform DELE command on connected host.
        Args:
            filename (str): Name of file to delete.
        Returns:
            Message from host.
        """
        self._check_is_connected()
        self._check_is_authenticated()

        self._send_command(FtpClient.DELE_COMMAND, filename)
        data = self._receive_command_data()

        return data

    def rmdir(self, directory):
        """
        Perform RMD command on connected host.
        Args:
            directory (str): Name of directory to delete.
        Returns:
            Message from host.
        """
        self._check_is_connected()
        self._check_is_authenticated()

        self._send_command(FtpClient.RMD_COMMAND, directory)
        data = self._receive_command_data()

        return data
