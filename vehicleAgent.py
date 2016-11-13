import os
import sys
import time
import unittest
import numpy as np
import itertools as it
import json
import spade


host = "127.0.0.1"

N = 10 # number of intersections

trad_graph = dict()

# roadmap = np.zeros((N,N), dtype=float)
# for i, j in it.combinations(range(N), 2):
#     roadmap[i][j] = float(np.random.randint(2, 10))

def agentID(agentName):
    return agentName+"@"+host


def initPosition():
    return np.random.randint(N)


def getCost(order, agentName):
    pickup, deliver = order
    return np.random.random()


def updatedTourPlan(path, tour, task):
    return path, tour


class PnEU(spade.Agent.Agent):

    def __init__(self, agentjid, password, company, speed=0.2):
        super(PnEU, self).__init__(agentjid, password)        
        self.company = company
        self.boss = agentID(company[0])
        self.speed = speed
        self.picked = {i: list() for i in range(N)}
        self.topick = {i: list() for i in range(N)}
        self.location = initPosition()
        self.path = [self.location,]
        self.tour = list()
  
    class BidForOrder(spade.Behaviour.Behaviour):
  
        def _process(self):
            ordermsg = self._receive(block=True,timeout=10)
            print "PnEU has received an order"
            myAgent = self.getAgent()

            # calculating cost
            jobid, task = json.loads(ordermsg.getContent())
            cost = getCost(task, myAgent.getName())

            # sending bid
            bidmsg = spade.ACLMessage.ACLMessage()
            bidmsg.setPerformative("inform")
            bossId = spade.AID.aid(myAgent.boss, ["xmpp://"+ myAgent.boss])
            bidmsg.addReceiver(bossId)
            bidmsg.setContent(json.dumps( (jobid, cost, task) ))
            bidmsg.setOntology("Bid")
            myAgent.send(bidmsg)
            print "PnEU has sent out a bid"

    class ReceiveGrant(spade.Behaviour.Behaviour):
        
        def _process(self):
            msg = self._receive(block=True,timeout=10)
            isgrant, jobid, task = json.loads(msg.getContent())
            print "PnEU bid has been "+isgrant.lower()
            if msg.isgrant() == "Granted":
                self.getAgent().modifyTour(jobid, task)
                # self.initiateTrade()

        def initiateTrade(self):
            myAgent = self.getAgent()
            initmsg = spade.ACLMessage.ACLMessage()
            initmsg.setPerformative("inform")
            bossId = spade.AID.aid(myAgent.boss, ["xmpp://"+ myAgent.boss])
            initmsg.addReceiver(bossId)
            initmsg.setOntology("InitTrade")
            myAgent.send(initmsg)
            print "PnEU has initiated Trading."


    class VehicleMotion(spade.Behaviour.PeriodicBehaviour):


        def _onTick(self):
            myAgent = self.getAgent()
            if myAgent.path and len(myAgent.path) > 1:
                print "Here2"
                i = myAgent.path.index(myAgent.location)
                nextstop = myAgent.path[1]
                self.traversed += self.speed
                distance = distmatrix[myAgent.location][nextstop] - self.traversed
                if distance < 0.0:
                    myAgent.path = myAgent.path[1:]

                    # have picked up all the orders on arriving at nextstop
                    if len(myAgent.topick[nextstop]):
                        for taskid, delivery in myAgent.topick[nextstop]:
                            myAgent.picked[delivery].append(taskid)

                    # striking out all the orders delivered at nextstop
                    if len(myAgent.picked[nextstop]):
                        for taskid in myAgent.picked[nextstop]:
                            print myAgent.getName(), " has completed task ", taskid
                        myAgent.picked[nextstop] = list()


    class RunTradeRound(spade.Behaviour.Behaviour):

        def onStart(self):
            self.aname = self.getAgent().getName()
        
        def _process(self):
            msg = self._receive(block=True,timeout=10)
            myAgent = self.getAgent()
            ST(self.aname, myAgent.tour, trad_graph)
            print "Ran one round of trading"
            msg = spade.ACLMessage.ACLMessage()
            msg.setPerformative("inform")
            msg.addReceiver(spade.AID.aid(myAgent.boss,["xmpp://"+myAgent.boss]))
            msg.setOntology("Trade")
            myAgent.send(msg)
            print "PnEU has sent a trade message."


    def modifyTour(self, jobid, task):
        self.path, self.tour = updatedPath(self.path, self.tour, task)
        self.topick[task[0]] = (jobid, task[1])

    def _setup(self):
        self.addBehaviour(self.VehicleMotion(1), None)
        template = spade.Behaviour.ACLTemplate()
        template.setSender(spade.AID.aid(self.boss, ["xmpp://"+self.boss]))
        template.setOntology("Order")
        t = spade.Behaviour.MessageTemplate(template)
        self.addBehaviour(self.BidForOrder(), t)

        template = spade.Behaviour.ACLTemplate()
        template.setSender(spade.AID.aid(self.boss, ["xmpp://"+self.boss]))
        template.setOntology("Grant")
        t = spade.Behaviour.MessageTemplate(template)
        self.addBehaviour(self.ReceiveGrant(), t)

        template.setOntology("TradeRound")
        t = spade.Behaviour.MessageTemplate(template)
        self.addBehaviour(self.RunTradeRound(), t)
        print "PnEU started!"
