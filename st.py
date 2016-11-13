import random
import numpy as np
import networkx as nx

def generateGraph(m,n):
	g=nx.grid_2d_graph(m,n)
	G=np.zeros((m*n,m*n))
	for i in g.edges():
		G[i[0][0]*n+i[0][1]][i[1][0]*n+i[1][1]]=random.randint(1,10)
		G[i[1][0]*n+i[1][1]][i[0][0]*n+i[0][1]]=G[i[0][0]*n+i[0][1]][i[1][0]*n+i[1][1]]
	return (g,G)

def cost(order,agentID,tourList):
	pickup,delivery=order
	t=list(tourList)
	t.remove(order)
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
	c=0
	for i in path:
		c+=G[i[0]][i[1]]
	return c/speed




sellingList=[]
def ST(agentID, tourList, TG):
	if random.random()<0.5: #Sell
		total=0
		for i in tourList:
			total+=cost(i,agentID,tourList)
		for i in range(len(tourList)):
			p[i]=cost(tourList[i],agentID,tourList)/total
			if cost(tourList[i],agentID,tourList)==0.0:
				p[i]=1.0/len(tourList)
		i=np.random.choice(len(tourList),1,p)[0]
		sellingList.append(tourList[i])
		TG[agentID].append('S',tourList[i],cost(tourList[i],agentID,tourList)
		tourList.remove(tourList[i])
	else:
		m=cost(sellingList[0],agentID,tourList)-cost(tourList[0],agentID,tourList) #Buy
		total=m
		for k in range(1,len(sellingList)):
			if cost(sellingList[k],agentID,tourList)-cost(tourList[k],agentID,tourList)<m:
				m=cost(sellingList[k],agentID,tourList)-cost(tourList[k],agentID,tourList)
			total+=cost(sellingList[k],agentID,tourList)-cost(tourList[k],agentID,tourList)
		for k in range(len(sellingList)):
			p[k]=(cost(sellingList[k],agentID,tourList)-cost(tourList[k],agentID,tourList)-m)/(total-k*m)
			if p[k]==0.0:
				p[k]=1/len(sellingList)
		k=np.random.choice(len(sellingList),1,p)[0]
		tourList.append(sellingList[k])
		TG[agentID].append('B',sellingList[i],cost(sellingList[i],agentID,tourList))
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
				findMaxMatch(i,j1,j2,g-cost(i,j2,tourList)+cost(i,k,tourList),Q)
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