import sys, os

if __name__ == "__main__":
	csvInput = open(sys.argv[1],"r")
	outFile = open(sys.argv[2],"w")
	lineNo = int(sys.argv[3])

	rawInput = csvInput.read()
	lines = rawInput.split('\n')

	if lineNo >= 0 and lineNo < len(lines):

		lines[lineNo] = lines[lineNo].split(',')

		outFile.write(",".join([line for line in lines[lineNo] if line.isdigit()]))

	csvInput.close()
	outFile.close()