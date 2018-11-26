import socket as mysoc
import sys


def fileLineCount(path):
	with open(path) as fileIn:
		for index, element in enumerate(fileIn):
			pass
	
	val = index + 1
	return val

# Check if arguments show up correctly
print ('Number of arguments:', len(sys.argv), 'arguments.')
print ('Argument List:', str(sys.argv))

# Socket with Client
try:
	ts = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
	print("[COM]: COM Server socket created")
except mysoc.error as err:
	print('{} \n'.format("COM socket open error ", err))

server_binding = ('', 65500)
ts.bind(server_binding)
ts.listen(1)





#FIXME must be changed later to do on different machine
host = mysoc.gethostname()
print("[COM]: COM Server host name is: ", host)
localhost_ip = (mysoc.gethostbyname(host))
print("[COM]: COM Server IP address is  ", localhost_ip)
csockid, addr = ts.accept()
print("[COM]: Got a connection request from to this server: ", addr)


if (len(sys.argv) == 2):
	DNS_COM_TXT = sys.argv[1]
else:
	DNS_COM_TXT = 'PROJ2-DNSCOM.txt'
	


# IMPORT FROM TS FILE HERE
inPath = DNS_COM_TXT
numLinesInFile = fileLineCount(inPath)
inFile = open(inPath, 'r')
print("Num Of Lines: " + str(numLinesInFile))

# Create Table
RSarr = [[] for _ in range(numLinesInFile)]

# fill in table
rowIndex = 0
while True:
	inLine = inFile.readline()
	if not inLine:  # if Line does not exist (EOF)
		break
	splitList = inLine.split()
	RSarr[rowIndex].append(splitList[0])
	RSarr[rowIndex].append(splitList[1])
	RSarr[rowIndex].append(splitList[2])
	rowIndex += 1

while 1:
	data_from_server = csockid.recv(100)
	
	if data_from_server:
		print("[COM]: Data recieved")
		findHost = data_from_server.decode('utf-8')
		print("[COM < RS] Data decoded from RS: [", findHost + "]")
		
		if (findHost == "Kill COM"):
			break
		
		foundHost = 0
		str = ""
		
		for i in range(numLinesInFile):
			if (RSarr[i][0] == findHost):
				print("FOUND HOST NAME")
				foundHost = 1
				str = RSarr[i][0] + " " + RSarr[i][1] + " " + RSarr[i][2]
				print("Going to send to RS" + str)
				break
		
		# send the result back
		if foundHost == 0:
			errorMessage = "Error"
			csockid.send(errorMessage.encode('utf-8'))
		else:
			print("Sending host name details now")
			csockid.send(str.encode('utf-8'))

# Close the server socket

print("[COM] Client told me to close. Goodbye!")
ts.close()
exit()

