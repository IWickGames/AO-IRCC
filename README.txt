AO-IRCC(Anonymous Online Internet Relay Chat Client) v1

An easy to setup public message service that makes it easy to have a simple public chat server
for users to connect on

Setup;
1.) Port forward 3323 on your router or server
2.) Install python 3.8.1 (Provided)
3.) In the "Server" folder locate settings.ini and under #bindIP change that to your local servers IP
4.) Start Server.py
Done!

Thats it now change the settings.ini for the client as well and compile it using auto-py-to-exe or pyinstaller
And make sure the new EXE is in the same folder as the settings.ini and run that. It will connect to your
Server and allow your users to pick a username they can use to be displayed as and be seen by other people

**Note that this does not encrypt the trapphic but it does stop IP logging by removing the IPS
**from its memory after there request is over and the IP's are never written to disk
**DO NOT RELY ON THIS FOR PROTECTED CHATS IT ONLY WILL MAKE EVERYONE ANONYMOUS BY STOPPING LOGGING
