import os
import re
import sys
import time
import socket
import argparse

# input argument
parser = argparse.ArgumentParser(description='CN_lab1')
parser.add_argument('-p', '--port',type=int)
parser.add_argument('-i', '--ip')
parser.add_argument('-f', '--folder',default='client_dir')
args = parser.parse_args()

if __name__ == '__main__':

  # create client dir
  if not os.path.exists(args.folder):
    try:
      os.makedirs(args.folder)
    except:
      sys.stderr.write("[ERROR] create {} directory".format(args.folder))
      sys.exit(1)
  os.chdir(args.folder)
  
  # client socket setting and connect
  try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((args.ip, args.port))
  except:
    sys.stderr.write("[ERROR] connect to server")
    sys.exit(1)

  # talk to server
  print 'connect to {} at port {}'.format(args.ip, args.port)
  while True:
    message = raw_input(">").strip()

    # no input
    if message == '':
      pass

    # command for lls
    elif message == 'lls':
      if '\n'.join(os.listdir('.')):
        print '\n'.join(os.listdir('.'))

    # command for lpwd
    elif message == 'lpwd':
      print os.getcwd()

    # command for lcd
    elif re.match('lcd\s+(.+)$',message):
      arg = re.match('lcd\s+(.+)$',message).group(1)
      try: os.chdir(arg)
      except: print 'something error when execute lcd {}'.format(cmd,arg)

    # command for put
    elif re.match('put\s+(.+)$',message):
      client_socket.send(message)  
      file_name = re.match('put\s+(.+)$',message).group(1)
      if os.path.isfile(file_name):
        f = open(file_name)
        while True:
          data = f.read(1024)
          if not data:
            break  
          client_socket.send(data)
        time.sleep(1)  
        client_socket.send("EOF")
        print client_socket.recv(1024)
      else:
        print 'file on client is not exist'
    
    # else
    else:  
      client_socket.send(message)
      recv = client_socket.recv(1024)
      if recv != ' ':
        print recv 


