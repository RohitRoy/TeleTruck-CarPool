import os
import sys
import time
import unittest
  
sys.path.append('../..')
  
import spade
  
host = "127.0.0.1"
  
  
class Company(spade.Agent.Agent):
  
    def _setup(self):
        self.addBehaviour(self.SendMsgBehav())
        template = spade.Behaviour.ACLTemplate()
        template.setSender(spade.AID.aid("b@"+host,["xmpp://b@"+host]))
        t = spade.Behaviour.MessageTemplate(template)
        self.addBehaviour(self.RecvMsgBehav(),t)
        print "Company started!"
  
    class SendMsgBehav(spade.Behaviour.OneShotBehaviour):
  
        def _process(self):
            msg = spade.ACLMessage.ACLMessage()
            msg.setPerformative("inform")
            msg.addReceiver(spade.AID.aid("b@"+host,["xmpp://b@"+host]))
            msg.setContent("testSendMsg")
            self.myAgent.send(msg)
  
            print "Company has sent a message:"
            print str(msg)

    class RecvMsgBehav(spade.Behaviour.OneShotBehaviour):
  
        def _process(self):
            msg = self._receive(block=True,timeout=10)
            print "Company has received a message:"
            print str(msg)
  
  
class PnEU(spade.Agent.Agent):
  
    class RecvMsgBehav(spade.Behaviour.OneShotBehaviour):
  
        def _process(self):
            msg = self._receive(block=True,timeout=10)
            print "PnEU has received a message:"
            print str(msg)

    class SendMsgBehav(spade.Behaviour.OneShotBehaviour):
  
        def _process(self):
            msg = spade.ACLMessage.ACLMessage()
            msg.setPerformative("inform")
            msg.addReceiver(spade.AID.aid("a@"+host,["xmpp://a@"+host]))
            msg.setContent("testSendMsg")
            self.myAgent.send(msg)
  
            print "PnEU has sent a message:"
            print str(msg)

    def _setup(self):
        self.addBehaviour(self.SendMsgBehav())
        template = spade.Behaviour.ACLTemplate()
        template.setSender(spade.AID.aid("a@"+host,["xmpp://a@"+host]))
        t = spade.Behaviour.MessageTemplate(template)
        self.addBehaviour(self.RecvMsgBehav(),t)
        print "PnEU started!"
  
  
a = Company("a@"+host,"secret")
b = PnEU("b@"+host,"secret","typ1")
c=PnEU("b@"+host,"secret","typ2")
  
b.start()
import time
time.sleep(1)
a.start()
time.sleep(1)
c.start()
  
alive = True
import time
while alive:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        alive=False
a.stop()
b.stop()
sys.exit(0)