import random
import numpy as np
import networkx as nx


def generateGraph(m,n):
	g=nx.grid_2d_graph(m,n)
	G=np.zeros((m*n,m*n)) + np.inf
	for i in g.edges():
		G[i[0][0]*n+i[0][1]][i[1][0]*n+i[1][1]]=random.randint(1,10)
		G[i[1][0]*n+i[1][1]][i[0][0]*n+i[0][1]]=G[i[0][0]*n+i[0][1]][i[1][0]*n+i[1][1]]
	return (g,G)


m, n = 10, 10
g, G = generateGraph(m, n)
N = m*n # number of intersections


def G_to_g(k):
    return (k/n, k%n)

def g_to_G(p):
	global n
	return p[0]*n + p[1]


def getcost(order,agent,tourList):
	speed = agent.speed
	curr_start = agent.path[1] if len(agent.path) > 1 else agent.path[0]
	curr_start = G_to_g(curr_start)
	# pickup, delivery = order
	t = list(tourList[:])
	if order in t:
		t.remove(order)
	else:
		t.append(order)
	ls=curr_start
	path=[]
	for i in tourList:
		p,d=i
		try:
			path.pop()
		except IndexError:
			pass
		path=path+nx.shortest_path(g,ls,p)
		path.pop()
		path=path+nx.shortest_path(g,p,d)
		ls=d
	c1=0
	for i in range(len(path) - 1):
		p1, p2 = g_to_G(path[i]), g_to_G(path[i+1])
		c1 += G[p1][p2]

	ls=curr_start
	path=[]
	for i in t:
		p,d=i
		try:
			path.pop()
		except IndexError:
			pass
		path=path+nx.shortest_path(g,ls,p)
		path.pop()
		path=path+nx.shortest_path(g,p,d)
		ls=d
	c2=0
	for i in range(len(path) - 1):
		p1, p2 = g_to_G(path[i]), g_to_G(path[i+1])
		# print "here5c3", path[i+1]
		c2 += G[p1][p2]
	return abs(c2 - c1)/speed


sellingList=[]
def ST(agentID, tourList, TG):
	if (len(sellingList) == 0 and len(tourList) == 0):
		return False
	p = [None]*len(tourList)
	if random.random()<0.5 and len(tourList) != 0: #Sell
		total = 0.0
		print "to Sell"+"\t"+str(agentID.getName())
		for i in tourList:
			total += getcost(i,agentID,tourList)
		for i in range(len(tourList)):
			p[i] = getcost(tourList[i],agentID,tourList) / total
			if getcost(tourList[i],agentID,tourList)==0.0:
				p[i]=1.0/len(tourList)
		i = np.random.choice(range(len(tourList)), 1, p)[0]
		sellingList.append(tourList[i])
		somecost = getcost(tourList[i],agentID, tourList)
		# print "no5"+str(somecost)
		TG[agentID].append(('S', tourList[i], somecost))
		# print "no6"
		tourList.remove(tourList[i])
		# print "no7"
		return True
	elif (len(sellingList) != 0):
		print "to Buy"+"\t"+str(agentID.getName())
		if (len(tourList)) == 0:
			p = [1.0 / len(sellingList)]*(len(sellingList))
		else:
			tourcostnow = getcost(tourList[-1], agentID, tourList)
			m = np.inf
			total = 0
			for k in range(0,len(sellingList)):
				if getcost(sellingList[k],agentID,tourList) - tourcostnow < m:
					m = getcost(sellingList[k],agentID,tourList) - tourcostnow
				total += getcost(sellingList[k],agentID,tourList) - tourcostnow
			# print "to2"
			denominator = total - (len(sellingList))*m
			if denominator == 0.0:
				p = [1.0 / len(sellingList)] * len(sellingList)
			else:
				for k in range(len(sellingList)):
					p[k] = (getcost(sellingList[k],agentID,tourList) - tourcostnow - m) / denominator
				if np.any(np.array(p) == 0.0):
					p = [1.0 / len(sellingList)] * len(sellingList)
			# print "to3"
		k = np.random.choice(len(sellingList),1,p)[0]
		tourList.append(sellingList[k])
		# print "toc"+str(k)+"\t"+str(TG.has_key(agentID))
		TG[agentID].append( ('B', sellingList[k], getcost(sellingList[k],agentID,tourList)) )
		# print "toc"+str(k)+"\t"+agentID.getName()
		# print "to4"
		# sellingList.remove(sellingList[k])
		return True
	return False

def findMaxMatch(i,l,k,g,Q):
	for j1 in range(l-1):
		for j2 in agentIDs:
			if M[j2][j1]==0:
				Q.append((i,l,k))
	if M[k][l]==0:
		M[k][l]=1
		for j1 in range(l-1):
			for j2 in agentIDs:
				M[j2][j1]=1
				findMaxMatch(i,j1,j2,g-getcost(i,j2,tourList)+getcost(i,k,tourList),Q)
	else:
		flag=0
		for p in Q:
			if M[p[2]][p[1]]==0:
				flag=1
				Q.remove(p)
				findMaxMatch(p[0],p[1],p[2],g,Q)
				Q.append(p)
		if flag==0:
			if g>g_max:
				g_max=g
				M_max=M
			for h in range(L):
				for r in agentIDs:
					if M[r][h]==0:
						if h==1 or M[r][h-1]==1:
							findMaxMatch(i,h,r,g,Q)
	M[k][l]=0
