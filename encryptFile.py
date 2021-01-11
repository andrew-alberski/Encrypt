#!usr/bin/env python3

import sys
#import numpy as np

README = """
README for encryptFile.py

GOALS:
	Make this File an excecutible
	Take in and read file(s) as argv and produce encryped file + key
	
Later down the raod: 
	Add decrypt flag
	Destroy passed file
"""

if(sys.argv[1] == "-h"):
	print (README)
	exit

### Encryption Functions ###
def convert_CHAR_to_ASCII(TEXT_TO_ENCRYPT):
	
	binary_list = []
	
	for line in TEXT_TO_ENCRYPT:
		for char in line:
			ascii_val = ord(char)
			binary_val = bin(ascii_val)
			binary_list.append(binary_val)

	return binary_list


### Decryption Functions ###
def convert_ASCII_to_CHAR(TEXT_TO_DECRYPT):
	
	char_list = []

	for val in TEXT_TO_DECRYPT:
		char_val = chr(int(val, 2))
		char_list.append(char_val)

	return char_list


if __name__ == "__main__":

	TEXT_TO_ENCRYPT = []
	FILES_TO_READ = []
	
	### Get Data in File(s) ###
	print("Files Found:")
	for i in sys.argv[1:]:
		print("\t" + i)
	print
	
	f = open(sys.argv[1], 'r')
	TEXT_TO_ENCRYPT = f.readlines()
	print (TEXT_TO_ENCRYPT)


	### Start Encryption ###
	binary_list = convert_CHAR_to_ASCII(TEXT_TO_ENCRYPT)
	print (binary_list)

	### Start Decryption ###
	char_list = convert_ASCII_to_CHAR(binary_list)
	print (char_list)
