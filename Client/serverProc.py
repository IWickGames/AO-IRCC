import os
from socket import *

#Client
def UDPClient(ipAddress, portSocket, strMessage):
    #Encode a string then send it in a packet
    addr = (ipAddress, portSocket)
    UDPSock = socket(AF_INET, SOCK_DGRAM)
    UDPSock.sendto(strMessage.encode(encoding="utf-8", errors='strict'), addr)
    UDPSock.close()

#Server
def UDPServer(ipAddress, portSocket, buffer=1024):
    #Wait untill a packet is resieved and then decode it and output it
    try:
        decode = ''
        addr = (ipAddress, portSocket)
        UDPSock = socket(AF_INET, SOCK_DGRAM)
        UDPSock.bind(addr)
        while decode == '':
            (data, addr) = UDPSock.recvfrom(buffer)
            decode = data.decode(encoding='utf-8', errors='strict')
        UDPSock.close()
    except KeyboardInterrupt:
        pass

    return str(addr[0]), str(addr[1]), decode; # Sender-IP, Sender-PORT, Decode

def TCPClient(ipAddress, portSocket, strMessage, buffer=1024):   
    client = socket() #Create Socket
    client.connect((ipAddress, portSocket)) #Connect to the Socket
    client.send(strMessage.encode("utf-8")) #Send packet
    data = client.recv(1024).decode("utf-8") #Capture responce packet
    client.close() #Close client
    return data; #Return data

def TCPServerRecieve(ipAddress, portSocket, buffer=1024):
    server = socket(AF_INET, SOCK_STREAM) #Create server socket
    server.bind((ipAddress, portSocket)) #Bind to IP and Port
    server.listen(1) #Wait for a connection
    conn, addr = server.accept() #Accept connection and store IP address
    data = conn.recv(buffer).decode("utf-8") #Get there message
    return conn, addr, data;

def TCPServerRespond(conn, strMessage):
    conn.send(strMessage.encode("utf-8")) #Echo the message back to the client to ensure it was resieved successfully
    conn.close() #Close socket