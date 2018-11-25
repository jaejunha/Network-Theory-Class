#!python3
'''
Code for 2018 Network Theory HW#2-2
'''
import networkx as nx
import matplotlib.pyplot as plt
import csv

# find negative cycle using dfs
def dfs(edges, start, now, path, bitmask, cost):
	
	# if find cycle
	if (len(path) > 1) and (start == now):

		# cost is negative
		if cost < 0:
			return path

		# cost is non-negative
		else:
			return []

	# already visited
	if bitmask & (1 << (int(now) - 1)):
		return []

	# not visited
	else:
		new_bitmask = bitmask | (1 << (int(now) - 1))
	
	for e in edges:
		# move to another node
		if e[0] == now:
			new_path = path
			new_path.append(e[1])
			solution = dfs(edges, start, e[1], new_path, new_bitmask, cost + int(edges[e]))
			
			# there is no cycle
			if len(solution) > 1:
				return solution
			
	# there is no cycle
	return []

def solve(filename):
	## Your
	## lines
	## of code
	## that TA will
	## use to check correctness
	
	G = nx.DiGraph()

	# open file
	file = open(filename)

	# read csv file
	contents = csv.reader(file)

	# Because first row is for description, need to skip
	next(contents)

	# save edges at G
	for i in contents:
		G.add_edge(i[0], i[1], weight = i[2])

	# make dictionary for edge information
	edges = dict([((u, v),d['weight'])
             for u,v,d in G.edges(data = True)])

	# After read contents, close file
	file.close() 
	
	
	# d is variable for distance	
	d = dict()
	
	# p is variable for precedence
	p = dict()

	# init distance and precedence variables
	for i in G.nodes:
		for j in G.nodes:
			p[(i, j)] = 0
			if i == j:
				d[(i, j)] = 0
			else:
				d[(i, j)] = 999

	for e in G.edges:
		d[(e[0], e[1])] = int(edges[(e[0], e[1])])
		p[(e[0], e[1])] = e[0]

	# refresh distance variable
	for k in G.nodes:
		for i in G.nodes:
			for j in G.nodes:
				if d[(i, j)] > d[(i, k)] + d[(k, j)]:
					d[(i, j)] = d[(i, k)] + d[(k, j)]
					p[(i, j)] = p[(k, j)]
	
	# print graph
	pos = nx.spring_layout(G)
	nx.draw(G, pos, with_labels = True)
	nx.draw_networkx_edge_labels(G, pos, edge_labels = edges)
	plt.show()

	cycle = False
	C = 0
	n = len(G.nodes)
	
	# find max weight
	for i in G.edges:
		if C < abs(int(edges[i])):
			C = (int(edges[i]))

	# check negative cycle
	for i in G.nodes:
		for j in G.nodes:
			if i == j:
				# if negative cycle exists
				if d[(i, j)] < 0:
					cycle = True
					break
			else:
				# if negative cycle exists
				if d[(i, j)] < - n * C:
					cycle = True
					break

		# if find negative cycle, don't need to check other nodes
		if cycle == True:
			break

	# if negative cycle exists
	if cycle == True:
		# find path which includes negative cycle using DFS method
		for i in G.nodes:
			path = []
			path.append(i)
			solution = dfs(edges, i, i, path, 0, 0)
			if len(solution) > 0: 
				return solution

	# if negative cycle doesn't exist
	else:
		solution = dict()
		for i in range(1, n + 1):
			for j in range(1, n + 1):
				if i == j:
					continue
				else:
					solution[(str(i), str(j))] = dict()

		for node in d.keys():
			if node[0] == node[1]:
				continue
			else:
				solution[node] = {"distance": d[node], "pred": p[node]}
		return solution

def main():
	# check file 1
	filename = "network_theory_hw2_graph1.csv"
	print(solve(filename))
		
	# check file 2
	filename = "network_theory_hw2_graph2.csv"
	print(solve(filename))

if __name__ == '__main__':
	main()
