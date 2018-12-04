import socket as mysoc
import socket
import hmac



def fileLineCount(path):
	with open(path) as fileIn:
		for index, element in enumerate(fileIn):
			pass
	
	val = index + 1
	return val


# second Socket
try:
	ts = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
	print("[TS]: Server socket created")
except mysoc.error as err:
	print('{} \n'.format("socket open error ", err))

server_binding = ('', 60000)
ts.bind(server_binding)
ts.listen(1)

#FIXME UNCOMMENT THIS LATER BC NEED TO FIX TO RUN ON MULTIPLE COMPUTERS
#host = "grep.cs.rutgers.edu"
host = mysoc.gethostname()
print("[TS]: TS Server host name is: ", host)
localhost_ip = (mysoc.gethostbyname(host))
print("[TS]: TS Server IP address is  ", localhost_ip)
csockid, addr = ts.accept()
print("[TS]: Got a connection request from a client to this server: ", addr)

#READ IN THE KEY HERE
TLDS1_KEY_TXT = 'PROJ3-KEY2.txt'
keyPath = TLDS1_KEY_TXT
keyFile = open(keyPath, 'r')
key = keyFile.readline()
print("****THE KEY IS: " + key);


# IMPORT FROM TS FILE HERE FOR TABLE
TLDS1_TXT = 'PROJ3-TLDS2.txt'
inPath = TLDS1_TXT
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
		print("[TLDS2]: Data recieved")
		challange = data_from_server.decode('utf-8')
		challange = challange.strip()
		print("[TLDS2 < RS] Data decoded from TLDS2 challange string: [" + challange + "]")
		
		# take the key [0] and the challange[1] and make the digest
		d1 = hmac.new(key.encode(), challange.encode("utf-8"))
		digest = d1.hexdigest()
		print("Digest in TLDS2 is: " + digest)
		csockid.send(digest.encode('utf-8'))
		
		# if (findHost == "Kill TS"):
		# 	break
		#
		#
		# foundHost = 0
		# str=""
		#
		#
		# for i in range(numLinesInFile):
		# 	if (RSarr[i][0] == findHost):
		# 		print("FOUND HOST NAME")
		# 		foundHost = 1
		# 		str = RSarr[i][0] + " " + RSarr[i][1] + " " + RSarr[i][2]
		# 		print("Going to send to client" + str)
		# 		break
		#
		# # send the result back
		# if foundHost == 0:
		# 	errorMessage = findHost + " - " + "Error:HOST NOT FOUND"
		# 	csockid.send(errorMessage.encode('utf-8'))
		# else:
		# 	print("Sending host name details now ts")
		# 	csockid.send(str.encode('utf-8'))

# Close the server socket

print("[TS] Client told me to close. Goodbye!")
ts.close()
exit()

