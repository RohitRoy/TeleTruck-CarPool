import random
import numpy as np
import networkx as nx

P = None
trad_graph = None
L = None
neighbours = None
Matchr = np.array([])
M_star = None

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
		c2 += G[p1][p2]
	return abs(c2 - c1)/speed


def ST(agentID, tourList, TG, sellingList):
	if (len(sellingList) == 0 and len(tourList) == 0):
		return False
	p = [None]*len(tourList)
	level=len(TG[agentID])
	if (random.random()<0.5 and len(tourList) != 0) or (level==0 and len(tourList)!=0): #Sell
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
		TG[agentID].append(('S', tourList[i], somecost))
		tourList.remove(tourList[i])
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
			denominator = total - (len(sellingList))*m
			if denominator == 0.0:
				p = [1.0 / len(sellingList)] * len(sellingList)
			else:
				for k in range(len(sellingList)):
					p[k] = (getcost(sellingList[k],agentID,tourList) - tourcostnow - m) / denominator
				if np.any(np.array(p) == 0.0):
					p = [1.0 / len(sellingList)] * len(sellingList)
		k = np.random.choice(len(sellingList),1,p)[0]
		tourList.append(sellingList[k])
		TG[agentID].append( ('B', sellingList[k], getcost(sellingList[k],agentID,tourList)) )
		return True
	return False


def findMaxMatch(i,l,k,g,Q, Matchr, neighbours, M_star):
	for j1 in range(l-1):
		if Matchr[i][j1]==0:
			Q.append((i,j1,trad_graph[P[i]][j1][1]))
	if Matchr[i][l]==0:
		Matchr[i][l]=1
		for n in neighbours[(i,l)]:
			Matchr[n[0]][n[1]]=1
			findMaxMatch(n[0],n[1],trad_graph[P[n[0]]][n[1]][1],g-trad_graph[P[i]][l][2]+trad_graph[P[n[0]]][n[1]][2],Q, Matchr, neighbours, M_star)
	else:
		flag=0
		for n in neighbours[(i,l)]:
			if Matchr[n[0]][n[1]]==0 and (n[0],n[1],trad_graph[P[n[0]]][n[1]][1]) in Q:
				flag=1
				Q.remove(p)
				findMaxMatch(n[0],n[1],trad_graph[P[n[0]]][n[1]][1],g,Q, Matchr, neighbours, M_star)
				Q.append(p)
		if flag==0:
			if g>g_star:
				g_star=g
				M_star *=  0.
				M_star += Matchr[:]
			for i1 in range(len(P)):
				for j1 in range(len(L)):
					if Matchr[i1][j1]==0:
						findMaxMatch(i1,j1,trad_graph[P[i1]][j1][1],g,Q, Matchr, neighbours, M_star)
	Matchr[i][l]=0
