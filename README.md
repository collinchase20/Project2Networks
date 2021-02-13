For this project I started by implementing the ability to parse the command line with the correct parameters.
This was fairly straightforward as we used the argument parsers from the last project. However, it did take a while
to do the processing on the parameters to distinguish a username, password, ftp url, port, and directory. I also had
to make the distinction between if a ftp url came before a local file and vise versa.

After this I established a connection to the server and played around with the FTP server in FileZila to get a better
understanding of it. To do this I had to establish a TCP connection for the control channel and send the apporopriate commands,
this was similar to the last project with sending and recieving commands from a socket so it was not troublesome.


Next I set out to implement the rmdir and mkdir commands. Also not very difficult as no data channel had to be established.
It was only a matter of sending the appropriate commands and the directory for which we were making or deleting.

Finally, the last couple of commands were ,much more difficult to implement. I had to open a second socket to process
the data for listing, copying, and moving files. Before that I had to send the FTP server the PASV command so that it would
 give me the IP address and port for which to open this data socket on. More importantly I had to learn how to send a file through sockets in python.
After some research on this it was clear I would need two main operations of reading and writing through the data channel
for the appropriate commands. From here you needed to disconnect the data socket before disconnecting the control socket.

To test my code I was initially using the khoury server but soon realized that simply using the terminal from PYCharm was much faster
and easier.
 
