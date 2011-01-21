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


import logging
import select
import socket
import uuid


LOG = logging.getLogger('seacreatures')
LOG.addHandler(logging.StreamHandler())
LOG.setLevel(logging.DEBUG)


class Connection(object):
    def __init__(self, server, port, nick, user, real):
        self.server = server
        self.port = port
        self.nick = nick
        self.user = user
        self.real = real
        self.channels = []
        self.sock = socket.socket()
        LOG.debug("CONNECTING TO %s:%i", self.server, self.port)
        self.sock.connect((self.server, self.port))
        LOG.debug(" * CONNECTED %s:%i", self.server, self.port)
        LOG.debug(" * LOGGING IN AS %s (%s:%s)", self.nick, self.user,
                  self.real)
        self.sock.send("NICK %s\r\n" % self.nick)
        self.sock.send("USER %s %s * :%s\r\n" % (self.user, self.server,
                                                 self.real))
    def join(self, chan):
        LOG.debug("JOINING: %s", chan)
        self.sock.send("JOIN :%s\r\n" % chan)
        # TODO(todd): should this check for a message to make sure we connected?
        self.channels.append(chan)

    def say(self, to, phrase):
        LOG.debug("SEPAKING TO irc://%s:%i/%s: %s", self.server, self.port,
                  to, phrase)
        self.sock.send("PRIVMSG %s :%s\r\n" % (to, phrase))
  

class SeaCreature(object):

    def __init__(self, default_nick=None, default_username='seacreature',
            default_realname='seacreature'):
        """Create a new (unconnected) seacreature.

        It will by default generate a nickname based on `uuid.uuid4`.
        You can connect it to multiple servers, see `connect`.
        Any server connection can join multiple rooms see `Connection#join`.

        You will want to subclass this method an overwrite the `handle_message`
        method.

        """
        self.connections = []
        if default_nick is None:
            self.default_nickname = uuid.uuid4().hex
        else:
            self.default_nickname = default_nick
        self.default_username = default_username
        self.default_realname = default_realname

    def connect(self, server='irc.freenode.net', port=6667,
                nickname=None, username=None, realname=None):
        nick = nickname or self.default_nickname
        user = username or self.default_username
        real = realname or self.default_realname
        connection = Connection(server, port, nick, user, real)
        LOG.debug("%r", connection)
        self.connections.append(connection)
        return connection

    def listen(self):
        # TODO(todd): use a selct timeout and tick() method to yield control
        #             back to bots occasionally.
        while 1:
            readsockets = [x.sock for x in self.connections]
            # TODO(todd): make sure > 0 sockets to listen for
            # TODO(todd): catch closed connections, exceptional connections
            LOG.debug("Calling select on %i connections", len(readsockets))
            readers, writers, exceptors = select.select(readsockets, [], [])
            LOG.debug("There are %i sockets to be read", len(readers))
            for socket in readers:
                connection = [x for x in self.connections
                                if x.sock == socket][0]
                LOG.debug("Receiving from irc://%s:%i", connection.server,
                          connection.port)
                self.receive(connection)

    def receive(self, connection):
        msg = ''
        msglen = 1024
        while msglen == 1024:
            new_msg = connection.sock.recv(1024)
            msg += new_msg
            msglen = len(new_msg)
            LOG.debug("Read %i bytes", msglen)
        LOG.debug(msg)
        lines = filter(None, msg.split("\n"))
        LOG.debug("%i lines in input", len(lines))
        for line in lines:
            # TODO(todd): Hanlde IRC Communications
            # TODO(todd): Use split(" ", 2) to get message type
            # TODO(todd): be sure we track #chan
            LOG.debug("LINE: %s", line)
            if (line.find(" PRIVMSG ") != -1):
                line = line.split(" PRIVMSG ")
                speaker = line[0].split("!")[0].replace(':', '')
                message = line[1].partition(' ')
                location = message[0]
                message = self._clean_message(message[2])
                LOG.debug("Handling message: %s on %s", speaker, location)
                self.handle_message(connection, location, speaker, message)

    def _clean_message(self, msg):
        message = msg.replace('\r', '')
        if message.startswith(":"):
            message = message[1::]
        return message

    def handle_message(self, connection, chan, user, message):
        """Re-implement this in your bots."""
        print "irc://%s:%i/%s: %s SAYS: %s" % (connection.server,
                                               connection.prot, chan, user,
                                               message)
