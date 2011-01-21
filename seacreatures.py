#                                               
#                                      _/_              
#         (   _  __,    _, _   _  __,  /  , , _   _  (  
#        /_)_(/_(_/(_  (__/ (_(/_(_/(_(__(_/_/ (_(/_/_)_
#                                               
#  a little Python library for creating interactive IRC creatures                                              
#             2011 Nikolai Warner | MIT License
#
#
#  1) Let's get creating! Import seacreatures and .join and .listen!
#  2) Make your creature do fun things? Yes! Go for it!
#  3) A humble beginning, but fork and push! Perhaps an ecosystem will arise?
#


import sys
import socket
import string

sock = socket.socket()
host = ""
channel = ""
nick = ""
username = ""
realname = ""


def join():  
    sock.connect((host, 6667))
    sock.send("NICK %s\r\n" % nick)
    sock.send("USER %s %s * :%s\r\n" % (username, host, realname))
    sock.send("JOIN :%s\r\n" % channel)



def say(something, to):
    sock.send("PRIVMSG %s :%s\r\n" % (to, something))
  
  
  
def listen(callback):
    transcript = ""
    
    while 1:
        message = ""
        location = ""
        speaker = ""
    
        transcript = transcript + sock.recv(1024)
        lines = transcript.split("\n")
        transcript = lines.pop()
  
        for line in lines:            
            if (line.find(" PRIVMSG ") != -1):            
                line = line.split(" PRIVMSG ")

                speaker = line[0].split("!")[0].replace(':', '')
                
                message = line[1].partition(' ')
                location = message[0]
                message = clean_message_string(message[2])
                
                callback({'speaker': speaker, 'location': location, 'message': message})
                
                

def clean_message_string(message):
    message = message.replace('\r', '')
    if message.startswith(":"):
        message = message[len(":"):]
    return message
     

            

