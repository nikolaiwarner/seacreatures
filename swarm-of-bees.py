#!/usr/bin/env python

import random
import seacreatures


class Beez(seacreatures.SeaCreature):
    def handle_message(self, connection, chan, user, message):
        print message
        if message.find("bee") != -1:
            connection.say(chan, self.random_beespeak())

    def random_beespeak(self):
        def ztimes():
            return "z" * random.randrange(1,10)
        return "b%s b%s b%s" % (ztimes(),ztimes(),ztimes())

 
swarm = Beez()

connection = swarm.connect(nickname="thehivex0r")
connection.join("#collexion")

swarm.listen()
