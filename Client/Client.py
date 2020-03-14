import os
import sys
import time
import keyboard
import ctypes
import urllib.request
import cursor

import serverProc

def getChat():
    rawData = serverProc.TCPClient(conIP, int(conPORT), "GET:CHAT")
    chatSplit = rawData.split("|-|-|")
    return chatSplit;

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

def msgBox(message):
    ctypes.windll.user32.MessageBoxW(0, message, "AO-IRCC", 0)

#Load settings
print("Loading Settings...")
settings = getSettings()

conIP = settings[0]
conPORT = settings[1]
headValue = settings[2]
maxDisplay = int(settings[3])

#Connect to the server
print("Connecting to server...")
try:
    messageList = getChat()
except Exception as error:
    #Could not connect try again!
    print("\n"*4)
    print("Could not connect to the server listed in settings.ini")
    print("Make sure that the IP and Port are correct or that the message server is online")
    print("\n")
    print("ERROR: " + str(error))
    input("\n")
    sys.exit()

#Create a username
validUser = False
while not validUser:
    username = input("Enter a username you want to use: ")

    if headValue in username:
        print("Packet header cant be in your username")
    else:
        validUser = True

#Connection was successfull now to start the client
messageListLen = 0
messageListLenTemp = 0

messageList = getChat()

update = False
while True:
    errorStatus = True
    messageListLenTemp = len(messageList)
    try:
        messageList = getChat()
        errorStatus = False
    except Exception as error:
        print("\n"*500)
        print("\n")
        print("Lost connection with server")
        print("ERROR: " + str(error))
        print("\n")

    if not errorStatus:
        MessageListLen = len(messageList)

        if messageListLen > messageListLenTemp:
            difference = messageListLen - messageListLenTemp
            msgBox(str(difference) + " new messages have are in your chat")

        #Display chat to the screen
        print('\n'*250)
        if len(messageList) >= maxDisplay:
            #Only display the max setting to the screen
            for i in range(len(messageList) - maxDisplay, len(messageList)):
                print(messageList[i])
        else:
            for obj in messageList:
                print(obj)

        #Display Text Box
        if update:
            time.sleep(0.5)
            update = False
        for i in range(0,100000):
            if keyboard.is_pressed("enter"):
                cursor.show()
                message = input('')
                message = input(str(username) + "> ")
                if not message == '':
                    #Encode and submit message
                    messageEncode = username + headValue + message
                    serverProc.TCPClient(conIP, int(conPORT), str(messageEncode))
                cursor.hide()
                update = True
                break