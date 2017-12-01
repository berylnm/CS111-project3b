#!usr/bin/python

import os

# global variables 
total_block = 0
total_inode = 0
block_size = 0
inode_size = 0

first_unreserved_block = 0
first_unreserved_inode = 0

# for block status block_status[i]
# block_status[i][0] = -2 if the block has been determined as duplicate at least once
# block_status[i][0] = -1 if unvisited by any function (i.e. reserved)
# block_status[i][0] = 0 if the block is on the freelist
# block_status[i][0] > 0 if the block is in use, in this case, block_status[i][0] = inode number, block_status[i][1] = block offset, block_status[i][2] = block type
block_status = []
inode_status = []

par_inode = 0
RFinode = 0
name = 0

exit_status = 0

# for reading lines to provide global constraint for each test module
# input: every line from the file
# output: directly update global variable
def constraints(line):

	global block_status
	global inode_status

	global total_block
	global total_inode
	global block_size
	global inode_size

	global first_unreserved_block
	global first_unreserved_inode
	

	if "SUPERBLOCK" in line:
		# split the line for read
		s_line = line.split(",",8)

		# meta data
		total_block = int(s_line[1])
		total_inode = int(s_line[2])
		block_size = int(s_line[3])
		inode_size = int(s_line[4])
		first_unreserved_inode = int(s_line[7])

		# initialize blocks
		block_status = [[(-1) for i in range(3)] for j in range(total_block)]

		# initialize inodes
		inode_status = [[-2, 0, 0] for j in range(0, first_unreserved_inode)]
		inode_status = [[-1, 0, 0] for j in range(first_unreserved_inode, total_inode)]

	elif "GROUP" in line:
		s_line = line.split(",",9)
		first_unreserved_block = int(line[8]) + math.ceil(float(inode_size) * total_inode / total_block)

	elif "BFREE" in line:
		s_line = line.split(",")
		block_status[int(s_line[1])][0] = 0	
	elif "IFREE" in line:
		s_line = line.split(",")
		block_status[int(s_line[1])][0] = 0		

# usage: after iterating through the constraint, pass each encountered block to this module
# input: see from variable name 
def invalid_block(blcok_num, block_type, inode, offset):
	global exit_status
	global block_status

	exit_status = 2

	invalid_inode(inode)
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

# do block check and inode check here
def parse_inode(line)
	
	global exit_status
	s_line = line.split(",")

	inode_num = int(s_line[1])
	invalid_inode(inode_num)

	for i in range(0, 15):
		block_num = int(s_line[12]) + i
		if i < 12:
			offset = i
			invalid_block(block_num, "BLOCK", inode_num, offset)
		elif i == 12:
			offset = i
			invalid_block(block_num, "INDIRECT BLOCK", inode_num, offset)
		elif i == 13:
			offset = 268
			invalid_block(block_num, "DOUBLE INDIRECT BLOCK", inode_num, offset)
		elif i == 14:
			offset = 65804
			invalid_block(block_num, "DOUBLE INDIRECT BLOCK", inode_num, offset)

# check if the inode is valid
def invalid_inode(inode)
	global inode_status
	global exit_status

	exit_status = 2
	if inode_status[inode][0] == 0:
		print("ALLOCATED INODE {0} ON FREELIST".format(inode))
	elif inode_status[inode][0] == -1:
		inode_status[inode][0] = 1  # not sure what to set here
	else:
		exit_status = 0


# check if the previous step has visited this block
def unreferenced blocks():

	global exit_status

	for i in range(first_unreserved_block, total_block):
		if block_status[i][0] == -1:
			exit_status = 2
			print("UNREFERENCED BLOCK {0}".format(i))

def Directory_Consistency_Audits(RFinode, par_inode, name):
	
	global exit_status

	if (RFinode > 0) and (RFinode <= total_inode):
		if (inode_status[RFinode - 1][0] > 0):
			inode_status[RFinode - 1][1] += 1
			if (inode_size[RFinode - 1][2] == 0):
				inode_status[RFinode - 1][2] = par_inode
		elif (inode_status[RFinode - 1][0] == 0):
			exit_status = 2
			print "DIRECTORY INODE {} NAME {} UNALLOCATED INODE {}".format(par_inode, name, RFinode)
	else:
		exit_status = 2
		print "DIRECTORY INODE {} NAME {} INVALID INODE {}".format(par_inode, name, RFinode)

	if (name == '.'):
		if (par_inode != RFinode):
			exit_status = 2
			print "DIRECTORY INODE {} NAME '.' LINK TO INODE {} SHOULD BE {}".format(par_inode, RFinode, par_inode)
	elif (name == '..'):
		if (RFinode != inode_status[par_inode - 1][2]):
			exit_status = 2
			print "DIRECTORY INODE {} NAME '..' LINK TO INODE {} SHOULD BE {}".format(par_inode, RFinode, inode_status[par_inode - 1][2])

def main():
	global exit_status

	if len(sys.argv) != 2
		sys.stderr.write("Usage: python lab3b [file name]")
		exit_status = 1
		sys.exit(exit_status)

	file = sys.argv[1]
		for line in file:
			if "SUPERBLOCK" in line or "GROUP" in line or "BFREE" in line or "IFREE" in line:
				constraints(line)
		for line in file:
			if "INODE" in line:
				parse_inode(line)
			if "DIRENT" in line:
				s_line = line.split(",")
				par_inode = int(s_line[1])
   				RFinode = int(s_line[3])
   				name = int(s_line[6])

				Directory_Consistency_Audits(RFinode, par_inode, name)

	# exit status should be updated during execution
	sys.exit(exit_status)

