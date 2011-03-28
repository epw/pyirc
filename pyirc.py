#! /usr/bin/env python

import sys, socket, re

def search (pattern, string):
    regex = re.search (pattern, string)
    if regex:
        return regex.group(1)
    else:
        return None

class IRC:
    readbuffer = ""

    def say (self, nick, msg):
        self.s.send ("PRIVMSG %s :%s\r\n" % (nick, msg))

    def reply (self, msgdata, msg):
        if msgdata[1] == self.CHAN:
            self.say (self.CHAN, msg)
        elif msgdata[1] == self.NICK:
            self.say (msgdata[0], msg)

    def action (self, nick, msg):
        self.s.send ("PRIVMSG %s :ACTION %s\r\n" % (nick, msg))

    def join (self, CHAN):
        print "Joining channel " + CHAN
        self.s.send ("JOIN :%s\r\n" % CHAN)

    def main (self):
        self.readbuffer = self.readbuffer + self.s.recv (1024)
        temp = self.readbuffer.split ('\n')
        self.readbuffer = temp.pop()
        action = False

        for line in temp:
            line = line.rstrip()
            line = line.split()

            if line[0] == "PING":
                self.s.send ("PONG %s\r\n" % line[1])
            elif line[1] == "PRIVMSG":
                nick = search (":([a-zA-Z_0-9']*)!", line[0])
                if nick:
                    reply = line[2]
                    message = ' '.join(line[3:])
                    message = message[1:]
                    if re.search ("ACTION .*", message):
                        message = search ("ACTION (.*)", message)
                        action = True
                    return (nick, reply, action, message)
                return None
            else:
                return ' '.join (line)
    
    def __init__ (self, HOST, PORT, NICK, REALNAME, CHAN=""):
        self.HOST = HOST
        self.PORT = PORT
        self.NICK = self.IDENT = NICK
        self.REALNAME = REALNAME

        self.s = socket.socket()
        print "Connecting to " + self.HOST + " on port " + str(self.PORT)
        self.s.connect ((self.HOST, self.PORT))
        print "Setting nickname " + self.NICK
        self.s.send ("NICK %s\r\n" % self.NICK)
        self.s.send ("USER %s %s bla :%s\r\n" % (self.IDENT, self.HOST,
                                                 self.REALNAME))
        self.CHAN = CHAN
        if CHAN:
            self.join (CHAN)

        print "Connected."
