import sys
import string



N = int (sys.argv[1])									# Physical memory size
inFile = sys.argv[2]									# File with input in notation R:1

class Page:											# Definition of page object
	def __init__(self, num):
		self.pID = num									# Page number
		self.ref = -1									# index of next access
		
def CheckMem (physM, virtP):								# Definition of function to verify if a page is in physical memory
	for page in physM:
		if page.pID == virtP.pID:
			return True
	return False

f = open(inFile, 'r')									# Access file with jobs

jobQ = f.read()										# Extract jobs
jobQ = jobQ.strip()
jobQ = jobQ.split()

f.close()												# Close file

phMem = []											# Emulates physical memory capacity
pageQ = []											# Order of page access
pFlt = 0												# Page fault counter

print "PageQ: ",
for j in jobQ:											# List access in pageQ
	j = j.split(":")[1]
	page = Page(int(j))
	pageQ.append(page)
	print page.pID,

for p in range(len(pageQ)):								# Set pages and verify space
	page = pageQ.pop(0)									# Page to enter physical memory
	print "\nPage to enter: ", page.pID,
	if (len(phMem) < N):								# Space available in physical memory 
		if(CheckMem (phMem, page)):						# Page already in physical memory
			print "\nPAGE HIT",
		else:										# Increase page fault counter and insert page
			print "\nPAGE FAULT",
			pFlt += 1
			phMem.append(page)
	else:											# Physical memory FULL
		print "\nPhysical Memory is full",
		if(CheckMem (phMem, page)):						# Page hit
			print "\nPAGE HIT",
		else:										# Increase page sault counter and find page to replace.
			print "\nPAGE FAULT",
			pFlt += 1
			to_remove = 0								# Physical memory index of page to remove
			nx_access = 0								# Index of next access
			for i in range(len(phMem)):
				print "\nitereating pM", phMem[i].pID,
				for p in range(len(pageQ)):
					print "\niterating vL", pageQ[p].pID,
					if (phMem[i].pID == pageQ[p].pID):
						print "\nmatchin IDs",
						phMem[i].ref = p				# Set reference attribute to index of next access
						print "\nbreak",
						break
				if (phMem[i].ref == -1):					# Page in physical memory not referenced again
					to_remove = i
					break
				elif (phMem[i].ref > nx_access):			# Determine longest access time
					nx_access = phMem[i].ref
					to_remove = i
				else:
					continue
			phMem.pop(to_remove)						# Remove longest access time
			phMem.append(page)							# Insert new page to physical memory
	print "\nphMem:"
	for x in phMem:
		print "ID:", x.pID, " Next access:", x.ref
	print "\npageQ:",
	for y in pageQ:
		print y.pID,
		
print "\nPysical Memory;",
for i in phMem:
	print i.pID,
print "\nPage Faults:", pFlt