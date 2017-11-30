#!usr/bin/python

import os

# global variables 
total_block = 0
total_inode = 0
block_size = 0
inode_size = 0

first_unreserved_block = 0

# for block status block_status[i]
# i[0] = exists on free list, i[1] = referenced 
block_status = []

exit_status = 0

# for reading lines to provide global constraint for each test module
# input: every line from the file
# output: directly update global variable
def constraints(line):

	global block_status
	global total_block
	global first_unreserved_block
	global block_size
	global inode_size
	
	fd = open(file, "r")
	for line in fd:
		if "SUPERBLOCK" in line:
			# split the line for read
			s_line = line.split(",",8)

			# meta data
			total_block = int(s_line[1])
			total_inode = int(s_line[2])
			block_size = int(s_line[3])
			inode_size = int(s_line[4])

			# initialize blocks
			block_status = [[(-1) for i in range(3)] for j in range(total_block)]

		elif "GROUP" in line:
			s_line = line.split(",",9)
			first_unreserved_block = int(line[8]) + math.ceil(float(inode_size) * total_inode / total_block)

		elif "BFREE" in line:
			s_line = line.split(",")
			block_status[int(s_line[1])][0] = 0		

# usage: after iterating through the constraint, pass each encountered block to this module
# input: see from variable name 
def invalid_block(blcok_num, block_type, inode, offset):
	global exit_status
	global block_status

	exit_status = 2

	if blcok_num < 0 or blcok_num >= total_block:
		print("INVALID {0} {1} IN INODE {2} AT OFFSET {3}".format(block_type, blcok_num, inode, offset))
	elif blcok_num < first_unreserved_block:
		print("RESERVED {0} {1} IN INODE {2} AT OFFSET {3}".format(block_type, blcok_num, inode, offset))
	elif block_status[i][0] > 0: 
		print("DUPLICATE {} {} IN INODE {} AT OFFSET {}".format(block_type, blcok_num, inode, offset))
		print("DUPLICATE {} {} IN INODE {} AT OFFSET {}".format(block_status[2], blcok_num, block_status[0], block_status[1]))
		block_status[i][0] = -2
	elif block_status[i][0] == 0 or block_status[i][0] == -1:
		if block_status[i][0] == 0:
			print("ALLOCATED BLOCK {0} ON FREELIST".format(blcok_num))
		block_status[0] = inode
		block_status[1] = offset
		block_status[2] = block_type
	else:
		exit_status = 0

# check if the previous step has visited this block
def unreferenced blocks():

	global exit_status

	for i in range(first_unreserved_block, total_block):
		if block_status[i][0] == -1:
			exit_status = 2
			print("UNREFERENCED BLOCK {0}".format(i))


def main():
	root_dir = '.'

	for files in os.listdir(root_dir):
		for file in files:
			if (file.endswith(".csv")):

