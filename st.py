import random
import numpy as np


def cost(itemID, agentID):
	pass

sellingList=[]
def ST(agentID, tourList, TG):
	if random.random()<0.5: #Sell
		total=0
		for i in tourList:
			total+=cost(i,agentID)
		for i in range(len(tourList)):
			p[i]=cost(tourList[i],agentID)/total
			if cost(tourList[i],agentID)==0.0:
				p[i]=1.0/len(tourList)
		i=np.random.choice(len(tourList),1,p)[0]
		sellingList.append(tourList[i])
		TG[agentID].append('S',tourList[i],cost(tourList[i])
		tourList.remove(tourList[i])
	else:
		m=cost(sellingList[0],agentID)-cost(tourList[0],agentID) #Buy
		total=m
		for k in range(1,len(sellingList)):
			if cost(sellingList[k],agentID)-cost(tourList[k],agentID)<m:
				m=cost(sellingList[k],agentID)-cost(tourList[k],agentID)
			total+=cost(sellingList[k],agentID)-cost(tourList[k],agentID)
		for k in range(len(sellingList)):
			p[k]=(cost(sellingList[k],agentID)-cost(tourList[k],agentID)-m)/(total-k*m)
			if p[k]==0.0:
				p[k]=1/len(sellingList)
		k=np.random.choice(len(sellingList),1,p)[0]
		tourList.append(sellingList[k])
		TG[agentID].append('B',sellingList[i],cost(sellingList[i]))
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
				findMaxMatching(i,j1,j2,g-cost(i,j2)+cost(i,k),Q)
	else:
		flag=0
		for p in Q:
			if M[p[2]][p[1]]==0:
				flag=1
				Q.remove(p)
				findMaxMatching(p[0],p[1],p[2],g,Q)
				Q.append(p)
		if flag==0:
			if g>g_max:
				g_max=g
				M_max=M
			for h in range(L):
				for r in agentIDs:
					if M[r][h]==0:
						if h==1 or M[r][h-1]==1:
							findMaxMatching(i,h,r)
	M[k][l]=0