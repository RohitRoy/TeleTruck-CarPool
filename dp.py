from itertools import chain, combinations, product
import numpy as np

m, n = 10, 10
g, G = generateGraph(m, n)
N = m*n # number of intersections


def G_to_g(k,n):
    return (k/n, k%n)

def g_to_G(p,n):
	return p[0]*n + p[1]

def permutations(iterable, r=None):
    pool = tuple(iterable)
    n = len(pool)
    r = n if r is None else r
    for indices in product(range(n), repeat=r):
        if len(set(indices)) == r:
            yield tuple(pool[i] for i in indices)

def powerset(iterable):
	xs = list(iterable)
	return chain.from_iterable( combinations(xs,n) for n in range(len(xs)+1) )

def getcost(a,b):
	global G
	global g
	global n
	path = nx.shortest_path(g,G_to_g(a,n),G_to_g(b,n))
	c=0
	for i in path():
		c+=G[a][b]
	return c

def getTime(orderList):
	perm = permutations(orderList)
	t=np.inf
	for i in perm:
		t_temp=np.random.randint(0,30)
		flag=0
		for j in i:
			if j[0]<t_temp:
				flag=1
				break
			t_temp+=getcost(j[1][0],j[1][1])
		if flag==0:
			if t_temp<t:
				t=t_temp
	return t

def DP(orderList,agentNo,curr_t):
	if (agentNo==1):
		curr_t+=getTime(orderList)
		return curr_t
	if len(orderList)==0:
		return curr_t
	best_t=np.inf
	allPossible = list(powerset(orderList))
	for i in allPossible:
		o=[]
		for j in orderList and j not in i:
			o.append(j)
		curr_t+=getTime(i,g)
		curr_t = DP(o,agentNo-1,curr_t)
		if curr_t<best_t:
			best_t=curr_t
	return best_t

