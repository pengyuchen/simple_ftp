import re
import os
import sys
import time
import socket
import argparse
from thread import *

# input argument
parser = argparse.ArgumentParser(description='CN_lab1')
parser.add_argument('-p', '--port',type=int)
parser.add_argument('-f', '--folder',default='server_dir')
args = parser.parse_args()

def threadWork(client, address):  
  print 'Client info {}'.format(address)
  while True:
    command = client.recv(1024)
    print "Client send: " + command

    # command ls
    if command == 'ls':
      if os.listdir('.') != []:
        client.send('\n'.join(os.listdir('.')))
      else:
        client.send(' ')

    # command pwd
    elif command == 'pwd':
      client.send(os.getcwd())
    
    # command mkdir
    elif re.match('mkdir\s+(.+)$',command):
      dir_name = re.match('mkdir\s+(.+)$',command).group(1)
      try:
        os.makedirs(dir_name) 
        client.send(' ')
      except:
        client.send('something error when execute mkdir {}'.format(dir_name))

    # command cd
    elif re.match('cd\s+(.+)$',command):
      path = re.match('cd\s+(.+)$',command).group(1)
      try:
        os.chdir(path) 
        client.send(' ')
      except:
        client.send('something error when execute cd {}'.format(path))

    # command rm
    elif re.match('rm\s+(.+)$',command):
      dir_name = re.match('rm\s+(.+)$',command).group(1)
      try:
        os.remove(dir_name)
        client.send(' ')
      except:
        client.send('something error when execute rm {}'.format(dir_name))
    
    # command put
    elif re.match('put\s+(.+)$',command):
      file_name = re.match('put\s+(.+)$',command).group(1)
      if os.path.isfile(file_name): os.remove(file_name)
      with open(file_name,'w') as f:
        while True:
          data = client.recv(1024)
          if data == 'EOF':
            break
          f.write(data)
        client.send('successfully upload file {}'.format(file_name))
    
    # command get
    elif re.match('get\s+(.+)$',command):
      file_name = re.match('get\s+(.+)$',command).group(1)
      if os.path.isfile(file_name):
        client.send('start download file...')
        time.sleep(1)
        with open(file_name) as f:
          while True:
            data = f.read(1024)
            if not data:
              break
            client.send(data)
        time.sleep(1)
        client.send('EOF')
      else:
        client.send('file on server is not exist')

    # else
    else:
      client.send("unknown command or error format")
  
  client.close()

if __name__ == '__main__':

  # create server dir
  if not os.path.exists(args.folder):
    try:
      os.makedirs(args.folder)
    except:
      sys.stderr.write("[ERROR] create {} directory".format(args.folder))
      sys.exit(1)
  os.chdir(args.folder)
  # server socket setting
  try:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #reuse tcp
    server_socket.bind(('', args.port))
    server_socket.listen(5)
  except:
    sys.stderr.write("[ERROR] socket setting")
    sys.exit(1)

  # start to listen
  print 'start listening on port {}'.format(args.port)
  while True:
    (client_socket, address) = server_socket.accept()
    start_new_thread(threadWork, (client_socket, address))
  svrver_socket.close()
