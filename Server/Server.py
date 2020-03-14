import os
import sys

import serverProc

#Create folders
if not os.path.exists("Webserver/chat.chatsave"):
    os.mkdir("Webserver")
    with open("Webserver/chat.chatsave", "w") as f:
        f.write("Welcome to the start of the Message Board. Start by typing something!\n")

def getSettings():
    commentChar = '#'

    #Get settings from settings file
    with open("settings.ini") as f:
        rawList = f.read().splitlines()
    
    removeComment = []
    for line in rawList:
        if not commentChar in line:
            removeComment.append(line)
    
    return removeComment;

def validate(rawData, head):
    valid = False
    checkHead = True

    if rawData == "GET:CHAT":
        valid = True
        checkHead = False

    if checkHead:
        #Split to head
        splitRawData = rawData.split(head)

        #Check if the header exists
        if head in rawData:
            valid = True
        else:
            valid = False
    
        #Check if there are to many heads
        if len(splitRawData) == 1:
            valid = False
        else:
            valid = True
    
    return valid;

print("Loading Settings...")
settings = getSettings()

#Header
headValue = settings[0]

#Python server settings
bindIP = settings[1]
bindPort = settings[2]
buffer = settings[3]
maxLength = settings[4]

print("Starting message server...")
lastSent = ''
while True:
    #Wait for a packet
    address = ''
    connt, address, rawPacket = serverProc.TCPServerRecieve(bindIP, int(bindPort), int(buffer))
    message = True

    if validate(rawPacket, headValue) and rawPacket == "GET:CHAT":
        message = False #Set message to load
        stringTMP = ''
        with open("Webserver/chat.chatsave") as f:
            tmp = f.read().splitlines() #Read chat file
        for i in tmp:
            stringTMP += i + "|-|-|"
        serverProc.TCPServerRespond(connt, stringTMP) #Send the chat to the client

    #Validate Packet
    if validate(rawPacket, headValue) and message:
        #Packet is valid! Check what it is

        #Check if the list is larger than the allowed length
        try:
            with open("Webserver/chat.chatsave") as f:
                tmp = f.read().splitlines()
            if len(tmp) > int(maxLength):
                os.remove("Webserver/chat.chatsave")
            
                with open("Webserver/chat.chatsave", "w") as f:
                    f.write("Welcome to the start of the Message Board. Start by typing something!\n")
            tmp = ''
        except:
            pass

        #Extract message
        if rawPacket != lastSent:
            splitPacket = rawPacket.split(headValue)
            print(splitPacket[0] + " POST " + splitPacket[1])
            with open("Webserver/chat.chatsave", "a") as f:
                f.write(splitPacket[0] + " :: " + splitPacket[1] + "\n")
            countBadPacket = 0
        else:
            #Packet Spam detected, start ignoring packets from them
            countBadPacket += 1

            splitPacket = rawPacket.split(headValue)
            print("HEAD: " + splitPacket[0] + " |  SPAM Behavior   COUNT[" + str(countBadPacket) + "]")
        
        serverProc.TCPServerRespond(connt, "POST SUCCESSFUL") #Return post message

        lastSent = rawPacket #Save last sent file