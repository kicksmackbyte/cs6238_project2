import os, subprocess
import sys
import crypt


if os.getuid() != 0:
	print("Please, run as root.")
	sys.exit()

uname = raw_input("Enter username : ")
passwd = raw_input("Enter Password for the " + uname + " : ")

flag=0

with open('/etc/shadow', 'r') as fp:	
	arr=[]

	for line in fp:
		temp = line.split(':')

		if temp[0] == uname:
			flag = 1

			salt_and_pass = temp[1].split('$')
			salt = salt_and_pass[2]

			result = crypt.crypt(passwd, '$6$' + salt)

			if result == temp[1]:
				print("Login successful.")     
			else:
				print("Invalid Password")
	
if flag == 0:
	print("User do not exist.")

