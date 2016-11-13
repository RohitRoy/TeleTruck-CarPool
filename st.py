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
	print "here"
	if (len(sellingList) == 0 and len(tourList)):
		return
	if random.random()<0.5 or len(sellingList) == 0: #Sell
		total=0
		print "no1"
		for i in tourList:
			total+=getcost(i,agentID,tourList)
		print "no2"
		for i in range(len(tourList)):
			p[i]=getcost(tourList[i],agentID,tourList)/total
			if getcost(tourList[i],agentID,tourList)==0.0:
				p[i]=1.0/len(tourList)
		print "no3"
		print "noc", range(len(tourList))
		print "nocd", np.random.choice( range(len(tourList)), 1, p)
		i = np.random.choice(range(len(tourList)), 1, p)[0]
		print "no4"
		sellingList.append(tourList[i])
		print "no5"
		TG[agentID].append('S',tourList[i],getcost(tourList[i],agentID,tourList))
		print "no6"
		tourList.remove(tourList[i])
		print "no7"
	else:
		print "to Buy"
		m=getcost(sellingList[0],agentID,tourList)-getcost(tourList[0],agentID,tourList) #Buy
		total=m
		print "to1"
		for k in range(1,len(sellingList)):
			if getcost(sellingList[k],agentID,tourList)-getcost(tourList[k],agentID,tourList)<m:
				m=getcost(sellingList[k],agentID,tourList)-getcost(tourList[k],agentID,tourList)
			total+=getcost(sellingList[k],agentID,tourList)-getcost(tourList[k],agentID,tourList)
		print "to2"
		for k in range(len(sellingList)):
			p[k]=(getcost(sellingList[k],agentID,tourList)-getcost(tourList[k],agentID,tourList)-m)/(total-k*m)
			if p[k]==0.0:
				p[k]=1/len(sellingList)
		print "to3"
		k=np.random.choice(len(sellingList),1,p)[0]
		tourList.append(sellingList[k])
		TG[agentID].append('B',sellingList[i],getcost(sellingList[i],agentID,tourList))
		print "to4"
		sellingList.remove(sellingList[i])

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