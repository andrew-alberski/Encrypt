#!usr/bin/python3

import sys
import numpy as np
import random as rand

README = """
README for encryptFile.py

Function: Read passed file and 'encrypt' data contents.
	  File to be encrypted should be passed in as argument (python3 encryptFile.py <file_to_be_coded.txt>)
	  Data will be coded and key will be given to decode the message.

Flags: -h 	Display this help and Exit

			
					----- Dev Notes -----
Encryption Process:
	DONE: (NOTE - All Done tasks also have an inverse decrypt function)

	1)Take message in as 1D list, then convert to a 'stack' of (3x3) matrices - using numpy arrays
	2)Convert the character values to ASCII binary
	3)Transpose each 3x3 matrix
	4)Right Shift ASCII values (ASCII value + key value)

	TODO:
	- Shuffle Stack of (3x3) arrays based on key
	- Further change individual 3x3 arrays, use linear algebra to shuffle columns / rows

GOALS:
	Make this File an excecutible (something going on with windows Linux env)
	Create -encrypt and -decrypt flags
	Destroy passed file so that only code and key exist (once finished)
"""

if(sys.argv[1] == "-h"):
	print (README)
	quit()

### Encryption Functions ###
def generate_Key():
	key_size = 8
	KEY = []
	
	for i in range(key_size): 
		KEY.append(chr(rand.randint(1,126)))
	
	return KEY

def convert_1Dlist_to_numpy3D(list_to_convert):
	N = int(len(list_to_convert) / 9) #Depth of (Nx3x3) matrix	
	if(len(list_to_convert) % 9 != 0):
		N += 1
		
		empty_val_idx = 9 - (len(list_to_convert) % 9) #num of empty values needed
		for i in range(empty_val_idx):
			list_to_convert.append(" ") #pad incomplete matrix
	
	#Numpy Array conversion to 3D
	np_arr = np.array(list_to_convert, dtype='object')
	np_arr = np_arr.reshape(int(N), 3, 3)

	return np_arr

def convert_CHAR_to_ASCII(np_charArr):	
		
	for val in np.nditer(np_charArr, flags=['refs_ok'], op_flags=['readwrite']):
		val[...] = str(bin(ord(str(val))))

	return

def do_transpose(np_arr, key_val): #Used for both encrypt and decrypt
	
	shape = np_arr.shape
	if (int(ord(key_val)) % 3 == 0):
		for i in range(shape[0]):
			tmp = np_arr[i].transpose()
			np_arr[i] = tmp
	
	return

def RightShift_ASCII_Values(np_arr, key_val):
	#shift for character values ONLY [32-126]
	
	shift_val = int(ord(key_val))

	if shift_val >= 94: #Catch circular shift
		shift_val = 5
	
	for val in np.nditer(np_arr, flags=['refs_ok'], op_flags=['readwrite']):
		if int(str(val), 2) >= 32 and int(str(val), 2) <= 126:
			tmp_val = int(str(val), 2) + shift_val
			
			if tmp_val > 126: #Wrap Around
				tmp_val = 32 + (tmp_val - 126)

			val[...] = str(bin(tmp_val))

	return

def LeftShift_ASCII_Values(np_arr, key_val):
	#shift for character range ONLY [32-126]
	
	shift_val = int(ord(key_val))

	if shift_val >= 94: #Catch circular shift
		shift_val = 5
	
	for val in np.nditer(np_arr, flags=['refs_ok'], op_flags=['readwrite']):
		if int(str(val), 2) >= 32 and int(str(val), 2) <= 126:
			tmp_val = int(str(val), 2) - shift_val
			
			if tmp_val < 32: #Wrap Around
				tmp_val = 126 - (32 - tmp_val)
				
			val[...] = str(bin(tmp_val))

	return

### Decrypt Functions ###
def convert_3Dnumpy_to_1Dlist(numpy_arr):
	list_1D = []

	for val in np.nditer(numpy_arr, flags=['refs_ok'], op_flags=['readwrite']):
		list_1D.append(str(val))	

	print ("\nDecryption: ")
	print (list_1D)
	return list_1D

def convert_ASCII_to_CHAR(np_charArr):
	
	for val in np.nditer(np_charArr, flags=['refs_ok'], op_flags=['readwrite']):
		val[...] = str(chr(int(str(val),2)))
	
	return


################
#     MAIN     #
################
if __name__ == "__main__":

	TEXT_TO_ENCRYPT = []
	
	np.set_printoptions(threshold=np.inf)

	### Get Data in File(s) ###
	print("Files Found:")
	for i in sys.argv[1:]:
		print("\t" + i)
	print
	
	f = open(sys.argv[1], 'r') #TODO: cycle through argv
	TEXT_TO_ENCRYPT = list(f.read())
	
	print("\nTEXT_TO_ENCRYPT: ")
	print(TEXT_TO_ENCRYPT)

	### Encrypt ###
	KEY = generate_Key()
	np_arr = convert_1Dlist_to_numpy3D(TEXT_TO_ENCRYPT)
	convert_CHAR_to_ASCII(np_arr)
	do_transpose(np_arr, KEY[1])
	RightShift_ASCII_Values(np_arr, KEY[2])
	
	print("\nEncryption ... (So far) : ")
	print(np_arr)

	### Decrypt ###
	LeftShift_ASCII_Values(np_arr, KEY[2])
	do_transpose(np_arr, KEY[1])
	convert_ASCII_to_CHAR(np_arr)
	convert_3Dnumpy_to_1Dlist(np_arr)
