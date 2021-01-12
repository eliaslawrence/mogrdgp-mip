#Author: Elias Lawrence

def open_file(file_name):	
	f = open(file_name, "r")
	return f

def close_file(f):	
	f.close()

def file_to_string(f):
	return f.read()

def print_file(f):	
	print(file_to_string(f))

def read_line(f):		
	return f.readline()

