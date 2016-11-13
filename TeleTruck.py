import os
import sys
import time
import unittest
import numpy as np
import itertools as it

import json
import spade

# sys.path.append('../..')

from vehicleAgent import *

A = 3 # number of agents

company = [str(a) for a in range(A+1)]

M = None

class Company(spade.Agent.Agent):
    """
    Agent to simulate the Transportation Company
    """

    class GenerateOrder(spade.Behaviour.PeriodicBehaviour):
        """
        To generate new orders periodically
        """
        
        def onStart(self):
            """
            Initiates order IDs
            """
            print "Starting Orders..."
            self.orders = 0

        def _onTick(self):
            """
            Generates new order of the form (OrderID, Task);
            where Task is of the form (PickupPoint, DeliveryPoint).
            """
            # generating new order
            print "Generating Order..."
            self.orders += 1
            pickup, deliver = initPosition(), initPosition()
            if pickup == deliver:
                deliver = (deliver+1)%N
            task = (pickup, deliver)

            # formulating message to delcare new order
            msg = spade.ACLMessage.ACLMessage()
            msg.setPerformative("inform")
            order = (self.orders, task)
            print "New Order:\t", order
            msg.setContent(json.dumps(order))
            msg.setOntology("Order")

            # informing vehicle agents about new order
            for b in company[1:]:
                msg.addReceiver(spade.AID.aid(agentID(b),["xmpp://" +agentID(b)]))
            self.getAgent().send(msg)
            print "Company has sent a new order."


    class SendMsgBehav(spade.Behaviour.OneShotBehaviour):
  
        def _process(self):
            msg = spade.ACLMessage.ACLMessage()
            msg.setPerformative("inform")
            msg.setContent("testSendMsg")
            msg.setOntology("Test")
            for b in company[1:]:
                msg.addReceiver(spade.AID.aid(agentID(b),["xmpp://" +agentID(b)]))
            self.getAgent().send(msg)
            print "Company has sent a message:"
            # print str(msg)


    class ReceiveBid(spade.Behaviour.Behaviour):
        """
        Receives bids from Vehicle agents in response to
        declaring a new order.
        Chooses the best bid and grants it the order.
        """
  
        def _process(self):
            # receive new bid and update bids for this order
            msg = self._receive(block=True, timeout=15)
            bids = self.getAgent().bids
            sender = msg.getSender().getName()
            jobid, bid, task = json.loads(msg.getContent())
            if not bids.has_key(jobid):
                bids[jobid] = dict()
            bids[jobid][sender] = bid # bid is the bidding price of sender
            print "Company has received a bid"

            if len(bids[jobid].keys()) == len(company)-1:
                print "Company has received all bids"

                # grant order to the best bidder
                minbidder = None
                minbid = np.inf
                for bidder, bid in self.getAgent().bids[jobid].iteritems():
                    print "Bidder: ", bidder
                    print "Bid: ", bid
                    if bid < minbid:
                        minbid = bid
                        minbidder = bidder
                print "Granting Order to ", minbidder
                self.grantOrder(jobid, task, minbidder)

                # delete granted job
                del self.getAgent().bids[jobid]
                print "Company has granted an order."

        def grantOrder(self, jobid, task, minbidder):
            """ Grant minbidder the order "jobid" for a task "task"
            """
            # sending grant message to minbidder
            grantmsg = self.generateMesg("Granted", jobid, task)
            grantmsg.addReceiver(spade.AID.aid(minbidder, ["xmpp://" + minbidder]))
            self.getAgent().send(grantmsg)

            # sending reject grant message to minbidder
            rejectmsg = self.generateMesg("Rejected", jobid, task)
            for b in company[1:]:
                if agentID(b) == minbidder: continue
                rejectmsg.addReceiver(spade.AID.aid(agentID(b),["xmpp://" +agentID(b)]))
            self.getAgent().send(rejectmsg)

        def generateMesg(self, isgrant, jobid, task):
            """ Utility: generate a message of the Grant format
            """
            msg = spade.ACLMessage.ACLMessage()
            msg.setPerformative("inform")
            msg.setOntology("Grant")
            content = json.dumps((isgrant, jobid, task))
            msg.setContent(content)
            return msg


    class InitiateTrade(spade.Behaviour.Behaviour):
        
        def _process(self):
            # receive new bid and update bids for this order
            msg = self._receive(block=True, timeout=15)
            print "Company has received request to trade"
            myAgent = self.getAgent()
            if myAgent.traderound == 0:
                for b in company[1:]:
                    trad_graph[b] = list()
                for b in np.random.shuffle(company[1:]):
                    trademsg = self.generateMesg(agentID(b))
                    myAgent.send(grantmsg)
                myAgent.traderound += 1
            else:
                print "Already trading. Ignoring request."

        def generateMsg(self, agentname):
            trademsg = spade.ACLMessage.ACLMessage()
            trademsg.setPerformative("inform")
            trademsg.setOntology("TradeRound")
            grantmsg.addReceiver(spade.AID.aid(agentname, ["xmpp://" + agentname]))
            return trademsg


    class PropagateTrade(spade.Behaviour.Behaviour):
  
        def _process(self):
            # receive new bid
            msg = self._receive(block=True, timeout=15)
            trades = self.getAgent().trades
            sender = msg.getSender().getName()
            trades.append(sender)
            print "Company has received a trading bid"

            if len(trades) == len(company)-1:
                print "Company has received all bids"
                if myAgent.traderound == 10:
                    print "Stopping Trade."
                    self.completeTrade()
                    print "Stopped Trading."
                else:
                    for b in company[1:]:
                        trad_graph[b] = list()
                    for b in np.random.shuffle(company[1:]):
                        trademsg = self.generateMesg(agentID(b))
                        myAgent.send(grantmsg)
                    myAgent.traderound += 1 # already started the i_th round

        def completeTrade(self):
            myAgent = self.getAgent()
            TG = myAgent.trad_graph
            M = np.zeros((len(company)-1, 10))
            for b in company[1:]:
                item = TG[0]
                #findMaxMatch()


        def generateMsg(self, agentname):
            trademsg = spade.ACLMessage.ACLMessage()
            trademsg.setPerformative("inform")
            trademsg.setOntology("TradeRound")
            grantmsg.addReceiver(spade.AID.aid(agentname, ["xmpp://" + agentname]))
            return trademsg


    def _setup(self):
        self.bids = dict()
        self.trades = list()
        self.traderound = 0
        self.addBehaviour(self.GenerateOrder(10))
        for b in company[1:]:
            template = spade.Behaviour.ACLTemplate()
            template.setSender(spade.AID.aid(agentID(b), ["xmpp://" + agentID(b)]))
            template.setOntology("Bid")
            t = spade.Behaviour.MessageTemplate(template)
            self.addBehaviour(self.ReceiveBid(), t)

            template.setOntology("InitTrade")
            t = spade.Behaviour.MessageTemplate(template)
            self.addBehaviour(self.InitiateTrade(), t)

            template.setOntology("Trade")
            t = spade.Behaviour.MessageTemplate(template)
            self.addBehaviour(self.PropagateTrade(), t)

        print "Company started!"


print "Here"
a = Company(agentID(company[0]), "secret")

print "Here"
P = list()
for b in company[1:]:
    P.append(PnEU(agentID(b), "secret", company))
P[-1].speed = 2.0
print "Made all Agents, ", len(P)

for b in P:
    b.start();
    b.roster.acceptAllSubscriptions();
    time.sleep(1)
a.start()
a.roster.acceptAllSubscriptions();
a.roster.followbackAllSubscriptions();

print "Ready to Accept \n"

for b in P:
    b.roster.subscribe(company[0]+"@"+host);
print "Subscribed! \n"

a.wui.start();
for b in P:
    b.wui.start();

try:
    for b in company[1:]:
        a.roster.addContactToGroup(agentID(b), "TruckAgents")
    print "Grouped! \n"
except BaseException as e:
    print e
    pass

print a.roster.getGroups(agentID(company[1]));

alive = True
while alive:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        alive=False

a.stop()
for b in P:
    b.stop()

sys.exit(0)