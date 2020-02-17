import os, subprocess
import sys
import getopt
from base64 import b64encode
import crypt


if os.getuid() != 0:
	print("Please, run as root.")
	sys.exit()

uname = raw_input("Enter Username you want to add: ")

with open('/etc/shadow','r') as fp:
	arr = []

	for line in fp:
		temp = line.split(':')

		if temp[0] == uname:
			print("user already exist. Try deleting it first.")
			sys.exit()

passwd = raw_input("Enter Password for the user: ")
re_passwd = raw_input("Renter Password for the user: ")

if passwd != re_passwd:
	print("Paswword do not match")
	sys.exit()

rand1 = os.urandom(6)
salt = str(b64encode(rand1).decode('utf-8'))

hash = crypt.crypt(passwd,'$6$' + salt)
line = uname + ':' + hash + ":17710:0:99999:7:::"

file1 = open("/etc/shadow", "a+")
file1.write(line+'\n')

try:
	os.mkdir("/home/" + uname)
except:
	print("Directory: /home/" + uname + " already exist")

file2 = open("/etc/passwd", "a+")

count = 1000				

with open('/etc/passwd', 'r') as f:
	arr1 = []

	for line in f:
		temp1 = line.split(':')

		while (int(temp1[3]) >= count and int(temp1[3]) < 65534):
			count = int(temp1[3]) + 1

count = str(count)

str1 = uname + ':x:' + count + ':' + count + ':,,,:/home/' + uname + ':/bin/bash' 

file2.write(str1)
file2.close()

file1.close()

