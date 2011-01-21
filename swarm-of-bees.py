#!/usr/bin/env python

import string
import random
import seacreatures



def random_beespeak():
    return "b%s b%s b%s" % (ztimes(),ztimes(),ztimes())
  
  
def ztimes():
    return "z" * random.randrange(1,10)


def listen_response(response):
    print response
    if (response['message'].find("bee") != -1):
        seacreatures.say(random_beespeak(), response['location'])
        
 
 
seacreatures.host =     "irc.freenode.net"
seacreatures.channel =  "#collexion"
seacreatures.nick =     "swarm-of-bees" 
seacreatures.username = "swarm-of-bees" 
seacreatures.realname = "swarm-of-bees"       
        
seacreatures.join()
seacreatures.listen(listen_response)
