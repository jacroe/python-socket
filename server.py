#!/usr/bin/env python
#TITLE:      Server program
#AUTHOR:     Jacob Roeland
#CLASS:      ITC 241
#DATE:       Nov 6, 2012
#USE:        python server.py
#OUTPUT:     None, unless the variable "debug" is set to True
import socket
import sys
import hashlib
import os

host = ''
port = 8000
debug = True

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if debug: print 'DEBUG:\t\tSocket created'
try:
  s.bind((host, port))
except socket.error, msg:
	print 'ERROR:\t\tBind failed. Error code : ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()

if debug: print 'DEBUG:\t\tSocket bind complete'

s.listen(10)
if debug: print 'DEBUG:\t\tSocket now listening on port ' + str(port) + '\n'

while 1:

	conn, addr = s.accept()
	if debug: print 'DEBUG:\t\tConnected with ' + addr[0] + ':' + str(addr[1])
	conn.sendall("Hi! I'm an authentication server!\n=================================\n")
	if debug: print 'DEBUG:\t\tSent welcome message'
	receipt = conn.recv(1024).rstrip()
	data = receipt.split("|")
	username = data[1]
	password = hashlib.sha256(data[2]).hexdigest()
	method = data[0]
	if method == "Reg" or method == "reg":
		if not os.path.exists(username):
			#open("data", "a").write("\n" + username + "|" + password)
			open(username, "w").write(password)
			if debug: print 'DEBUG:\t\t' + username + ' was registered'
			conn.sendall(username + " was registered succesfully!")
		else:
			if debug: print 'DEBUG:\t\tTried to register ' + username + ' but that user already exists'
			conn.sendall(username + " has already been registered. Try Auth")
	elif method == "Auth" or method == "auth":
		if os.path.exists(username) and password == open(username, 'r').read():
			if debug: print 'DEBUG:\t\t' + username + ' succeeded authenticating'
			conn.sendall('Success!')
		else:
			if debug: print 'DEBUG:\t\t' + username + ' failed authenticating'
			conn.sendall('Fail!')
	else:
		if debug: print 'DEBUG:\t\tNot a supported method'
		conn.sendall('"' + method + '" is not a supported method')
	if debug: print 'DEBUG:\t\tClosed connection with ' + addr[0] + ':' + str(addr[1]) + '\n'
	conn.close()
	

s.close()
