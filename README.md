# simple FTP
A server program and client program with python socket for transferring files.
The client is able to download a file from the server or upload a file to the server through a TCP socket.

## Server
Run the following command:
```
python server.py -p <port>
```
`port` is a port number where the server will listen on this port. 

## Client
Run the following command:
```
python server.py -i <ip> -p <port>
```
`ip` and `port` is the IP address and port number to the server

## Usage
- put [filename] : upload a file to the server’s working directory. If thename of the file already exists, overwrite the file.
- get [filename] : download a file from the server and store in the client’s working directory. If the name of the file already exists,overwrite the file.
- mkdir [name] : make a directory in server’s working directory.
- ls : list the files in server’s working directory.
- lls : list the files in client’s working directory.
- pwd : print out server’s working directory.
- lpwd : print out client’s working directory.
- rm [filename] : remove a file named “filename” in server’s working directory
- cd [directory name] : change server’s working directory. 