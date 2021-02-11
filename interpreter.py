import os
from cmd import Cmd
from client import FtpClient


class FtpInterpreter():
    """
    FTP client command line utility.
    """
    def __init__(self):
        self._ftp_client = FtpClient()

    def _update_prompt(self):
        prompt = 'FTP'
        if self._ftp_client.host is not None:
            prompt = '{} {}'.format(prompt, self._ftp_client.host)
            if self._ftp_client.user is not None:
                prompt = '{} ({})'.format(prompt, self._ftp_client.user)
        self.prompt = '{} > '.format(prompt)

    def _perform_ftp_command(self, command, *args):
        print("we are here")
        method = getattr(self._ftp_client, command)
        print(method)
        try:
            response = method(*args)
        except:
            response = "Invalid Response When Performing Command"

        return response

    def emptyline(self):
        pass

    def do_connect(self, host):
        """
        Command to connect to an FTP server in the specified host.
        Args:
            host (str): The host to connect to.
        """
        response = self._perform_ftp_command('connect', host)
        print("This is the connect response")
        print(response)
        self._update_prompt()


    def do_disconnect(self):
        """
        Command to disconnect from connected FTP host.
        """
        response = self._perform_ftp_command('disconnect')
        print("This is the disconnect response")
        print(response)
        self._update_prompt()

    def do_login(self, user, password):
        """
        Command to login with user and password in the connected FTP host.
        """
        response = self._perform_ftp_command('login', user, password)
        print("This is the login response")
        print(response)
        self._update_prompt()


    def do_list(self, filename):
        """
        Command to perform LIST command on the connected FTP host.
        Args:
            filename (str): Name of file or directory to retrieve info for.
        """
        response = self._perform_ftp_command('list', filename)
        print(response)


    def do_mkdir(self, directory):
        """
        Command to create directory on the connected FTP host.
        Args:
            directory (str): Name of directory to create.
        """
        response = self._perform_ftp_command('mkdir', directory)
        print(response)

    def do_rm(self, filename):
        """
        Command to remove file on the connected FTP host.
        Args:
            filename (str): Name of file to delete.
        """
        response = self._perform_ftp_command('rm', filename)
        print (response)

    def do_rmdir(self, directory):
        """
        Command to remove directory on the connected FTP host.
        Args:
            directory (str): Name of directory to delete.
        """
        response = self._perform_ftp_command('rmdir', directory)
        print (response)