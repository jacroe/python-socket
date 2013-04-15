#!/usr/bin/env python
#TITLE:  	Client program
#AUTHOR:	Jacob Roeland
#CLASS:		ITC 241
#DATE:		Nov 6, 2012
#USE:		python client.py localhost 8000 [Reg|Auth] Username Password
#OUTPUT:	The output from the server, specifically if registering or authenticating was successful; more if "debug" is on		

import socket
import sys

debug = False

if len(sys.argv) != 6:
	print 'ERROR:\t\tWrong number of arguments'
	print str(sys.argv)
	print '\t\tclient.py [ServerIp] [ServerPort] [Reg|Auth] [Username] [Password]'
	sys.exit()
host = sys.argv[1]
port = int(sys.argv[2])
message = sys.argv[3] + "|" + sys.argv[4] + "|" + sys.argv[5]

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
	print 'ERROR:\t\tFailed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
	sys.exit()
if debug: print 'DEBUG:\t\tSocket Created'
try:
	remote_ip = socket.gethostbyname( host )
except socket.gaierror:
	print 'ERROR:\t\tHostname could not be resolved. Exiting'
	sys.exit()
if debug: print 'DEBUG:\t\tIP addres of ' + host + ' is ' + remote_ip
try:
	s.connect((remote_ip, port))
except socket.error:
	print 'ERROR:\t\tConnection to ' + host + ':' + str(port) + ' refused'
	sys.exit()
if debug: print 'DEBUG:\t\tSocket connected to ' + host + ' on ip ' + remote_ip
print s.recv(256)
if debug: print 'DEBUG:\t\tAttempting to send "' + message + '"'
try:
	s.sendall(message)
except socket.error:
	print 'ERROR:\t\tSend failed'
	sys.exit()
if debug: print "DEBUG:\t\tMessage sent successfully"
print s.recv(2056)
s.close()
