import socket as mysoc
import hmac
import sys


def fileLineCount(path):
	with open(path) as fileIn:
		for index, element in enumerate(fileIn):
			pass
	
	val = index + 1
	return val

# Socket with AS
try:
	ts = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
	print("[TLDS1]: TLDS1 Server socket created")
except mysoc.error as err:
	print('{} \n'.format("TLDS1 socket open error ", err))

server_binding = ('', 65500)
ts.bind(server_binding)
ts.listen(1)

# Socket with C
try:
	ts_client = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
	print("[TLDS1]: TLDS1 Server socket for CLIENT created")
except mysoc.error as err:
	print('{} \n'.format("TLDS1 socket open error ", err))

serverClient_binding = ('', 40000)
ts_client.bind(serverClient_binding)
ts_client.listen(1)



#FIXME must be changed later to do on different machine
host = mysoc.gethostname()
print("[TLDS1]: TLDS1 Server host name is: ", host)
localhost_ip = (mysoc.gethostbyname(host))
print("[TLDS1]: TLDS1 Server IP address is  ", localhost_ip)
csockid, addr = ts.accept()
print("[TLDS1]: Got a connection request from to this server: ", addr)

#READ IN THE KEY HERE
TLDS1_KEY_TXT = 'PROJ3-KEY1.txt'
keyPath = TLDS1_KEY_TXT
keyFile = open(keyPath, 'r')
key = keyFile.readline()
print("****THE KEY IS: " + key);


# IMPORT FROM TS FILE HERE FOR TABLE
TLDS1_TXT = 'PROJ3-TLDS1.txt'
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


clientConnected = False
while 1:
	data_from_server = csockid.recv(100)
	
	if data_from_server:
		msg = data_from_server.decode('utf-8')
		if msg == "Sending Challenge":
			print("===== Challenge ====")
			# Acknowledge
			csockid.send("Ready".encode('utf-8'))
			# Get Challenge from AS
			data_from_server = csockid.recv(100)
			challange = data_from_server.decode('utf-8')
			challange = challange.strip()
			print("[TLDS1 < AS] Data decoded from TLDS1 challange string: [" + challange + "]")
			
			# take the key [0] and the challange[1] and make the digest
			d1 = hmac.new(key.encode(), challange.encode("utf-8"))
			digest = d1.hexdigest()
			print("[TLDS1 > AS] Digest in TLDS1 is: " + digest)
			csockid.send(digest.encode('utf-8'))
			
			# next instruction
			msg = csockid.recv(1024).decode('utf-8')
			print("[TLDS1 < AS]: Next instruction: " + str(msg))
			print("")
			
		if msg == "WaitForClient":
			print("CLIENT CONNECTION")
			
			if clientConnected == False:
				clientConnected = True
				cclientid, addr1 = ts_client.accept()
				print("[TLDS1]: Got a connection request from to this server: ", addr1)
			work = cclientid.recv(1024).decode('utf-8')
			print("[TLDS1 < AS]: should be that this is client: " + str(work))
			cclientid.send("Ready for Host Name".encode('utf-8'))
			print("SENT READY FOR HOST")
			msg = cclientid.recv(1024).decode('utf-8')
			print("[TLDS1 < Client]: Message recieved that is host[" + msg)
			# send back correct answer
			# FIXME RETURN IP ADDRESS HERE
		
			foundHost = 0
			st = ""

			for i in range(numLinesInFile):
				print("Currently looking at["+RSarr[i][0]+"] VS CURRENT HOST ["+msg+"]")
				if (RSarr[i][0] == msg):
					print("FOUND HOST NAME")
					foundHost = 1
					st = RSarr[i][0] + " " + RSarr[i][1] + " " + RSarr[i][2]
					print("Going to send to client" + st)
					break
			# send the result back
			if foundHost == 0:
				errorMessage = "Error: HOST NOT FOUND"
				print("sending error")
				cclientid.send(errorMessage.encode('utf-8'))
			else:
				print("Sending host name details now ts")
				cclientid.send(st.encode('utf-8'))
				
		  
			#cclientid.send("CORRECT ANSWER".encode('utf-8'))
			#print("[TLDS1 > Client]: Correct answer sent")
			
			print(" ")
			
			#cclientid.close()
		
		if msg == "Terminate":
			break;
		
		
	
	
		
		# if (findHost == "Kill COM"):
		# 	break
		#
		# foundHost = 0
		# str = ""
		#
		# for i in range(numLinesInFile):
		# 	if (RSarr[i][0] == findHost):
		# 		print("FOUND HOST NAME")
		# 		foundHost = 1
		# 		str = RSarr[i][0] + " " + RSarr[i][1] + " " + RSarr[i][2]
		# 		print("Going to send to RS" + str)
		# 		break
		#
		# # send the result back
		# if foundHost == 0:
		# 	errorMessage = "Error"
		# 	csockid.send(errorMessage.encode('utf-8'))
		# else:
		# 	print("Sending host name details now")
		# 	csockid.send(str.encode('utf-8'))

# Close the server socket

print("[TLDS1] AS told me to close. Goodbye!")
ts_client.close()
ts.close()
exit()

