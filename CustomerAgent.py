import spade
import time

host = "127.0.0.1"

class Sender(spade.Agent.Agent):

    def _setup(self):
        self.addBehaviour(self.SendMsgBehav())
        print "Agent started!"
        
    class SendMsgBehav(spade.Behaviour.OneShotBehaviour):
        """
        This behaviour sends a message to this same agent to trigger an EventBehaviour
        """

        def _process(self):
            msg = spade.ACLMessage.ACLMessage()
            msg.setPerformative("inform")
            msg.addReceiver(spade.AID.aid("a@"+host,["xmpp://a@"+host]))
            msg.setContent("testSendMsg")
            print "Sending message in 3 . . ."
            time.sleep(1)
            print "Sending message in 2 . . ."
            time.sleep(1)
            print "Sending message in 1 . . ."
            time.sleep(1)

            self.myAgent.send(msg)
            
            print "I sent a message"
            #print str(msg)
    
    class RecvMsgBehav(spade.Behaviour.EventBehaviour):
        """
        This EventBehaviour gets launched when a message that matches its template arrives at the agent
        """

        def _process(self):            
            print "This behaviour has been triggered by a message!"
            
    
    def _setup(self):
        # Create the template for the EventBehaviour: a message from myself
        template = spade.Behaviour.ACLTemplate()
        template.setSender(spade.AID.aid("a@"+host,["xmpp://a@"+host]))
        t = spade.Behaviour.MessageTemplate(template)
        
        # Add the EventBehaviour with its template
        self.addBehaviour(self.RecvMsgBehav(),t)
        
        # Add the sender behaviour
        self.addBehaviour(self.SendMsgBehav())  
    

if __name__ == "__main__":
    a = Sender("agent@127.0.0.1", "secret")
    a.start()