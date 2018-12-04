import socket as mysoc
import hmac

import sys

def fileLineCount(path):
	with open(path) as fileIn:
		for index, element in enumerate(fileIn):
			pass
	
	val = index + 1
	return val


# FIRST Socket | to RS server
try:
	rs = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
	print("[C]: Socket for RS created")
except mysoc.error as err:
	print('{} \n'.format("socket open error ", err))
	
# # SECOND SOCKET
# try:
# 	ts = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
# 	print("[C]: Socket for TS created")
# except mysoc.error as err:
# 	print('{} \n'.format("TS socket open error ", err))

DNS_HNS_TXT = 'PROJ3-HNS.txt'

#Port for RS
RsPort = 50020

# Client Host/IP setup
clientHost = mysoc.gethostname()
print("[C]: Client name is: " , clientHost)
clientIP = mysoc.gethostbyname(mysoc.gethostname())
print("[C]: Client IP is: " , clientIP)

# connect to RS_SERVER
rs_ip = mysoc.gethostbyname(mysoc.gethostname())
print(rs_ip)
server_bindingRS = (rs_ip, RsPort)
rs.connect(server_bindingRS) # RS will be waiting for connection
print ("[C]:  Connected to RS Server")


# Import from file
inPath = DNS_HNS_TXT
numLinesInFile = fileLineCount(inPath)
inFile = open(inPath, 'r')
print("Num Of Lines in HNS: " + str(numLinesInFile))

rs.send(str(numLinesInFile).encode('utf-8'))
data_from_server = rs.recv(100)
msg = data_from_server.decode('utf-8')
print("[C < RS]: Response: " + msg)
# send num of lookups

#create a file to output the data
fileOut = open("Resolved.txt", "w")
tsConnected = False
while True:
	# Each iteration = one lookup in TS/RS
	inLine = inFile.readline()
	if not inLine:
		break
	
	# Send line to RS
	inLine = inLine.strip('\n')
	splitList = inLine.split()
	#take the key [0] and the challange[1] and make the digest
	d1 = hmac.new(splitList[0].encode(), splitList[1].encode("utf-8"))
	digest = d1.hexdigest()
	challange = splitList[1].strip()
	
	#now send the challange string [1] and the dijest
	rs.send(challange.encode('utf-8'))
	print("[C > RS] Line Sent: ["+challange +"]")
	rs.send(digest.encode('utf-8'))
	print("[C > RS] Line Sent: " + digest)


	data_from_server = rs.recv(1024)
	msg = data_from_server.decode('utf-8')
	print("[C < RS]: Response : " + msg)
	
	# if msg == "TLDS1":
	# 	if not TLDS1HostConnected:
	# 		TLDS1HostConnected = True
	# 		TLDS1Port = 40000
	# 		TLDS1_ip = mysoc.gethostbyname(TLDS1HostName)
	# 		server_bindingTLDS1 = (TLDS1_ip, TLDS1Port)
	# 		TLDS1.connect(server_bindingTLDS1)
	# 		print("[C]: Connected to TLDS1 Server")
	#
	# 	# send the hostname to both TLDS Servers 1
	# 	print("[C > TLDS1] sending: " + challange)
	# 	TLDS1.send(splitList[2].encode('utf-8'))
	# 	data_from_TLDS1 = TLDS1.recv(1024)
	# 	print("[C < TLDS1] received:  ", data_from_TLDS1.decode('utf-8'))
	# 	msgTLDS1 = data_from_TLDS1.decode('utf-8')
	# if not TLDS2HostConnected:
	# 	TLDS2HostConnected = True
	# 	TLDS2Port = 60000
	# 	TLDS2_ip = mysoc.gethostbyname(TLDS2HostName)
	# 	server_bindingTLDS2 = (TLDS2_ip, TLDS2Port)
	# 	TLDS2.connect(server_bindingTLDS2)
	# 	print("[C]: Connected to TLDS1 Server")

	# # output the string to result file
	# strToFile = msg + "\n"
	# fileOut.write(strToFile)
	# print("[C]: Line is VALID: ", msg)

	print("")


#do not uncomment below
#ts.send("Kill TS".encode('utf-8'))

rs.close()
#do not uncomment belo
#ts.close()




#print("Stuff ended")
#data_from_server = rs.recv(1024)
#print("[C]: Data received from RS server: [", data_from_server.decode('utf-8'), "]")
#data_from_server_decoded= data_from_server.decode('utf-8')







