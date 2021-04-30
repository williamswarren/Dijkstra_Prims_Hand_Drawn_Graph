colors_dict = {"red":[237,51, 35],
	"green":[114, 249, 76],
	"purple":[146, 60, 231],
	"orange":[245, 167, 60],
	"pink":[247, 195, 203],
	"yellow":[255, 252, 84],
	"green":[114, 249, 76],
	"white":[255, 255, 255],
	"black":[0, 0, 0]}

letters_dict = {"red":"A",
		"green":"G",
		"purple":"C",
		"orange":"D",
		"pink":"E",
		"yellow":"F",
		"green":"G"}

visited = {}
'''
#psuedo code

#def vertice_edge_finder():

for i in range(rows):
    for j in range(columns):
	if mat[i][j] in colors_dict and color has not been visited/discovered:
		mark mat[i][j] as visited
		put adjacent pixels in queue
		initiate BFS
		if we hit a pixel that is close to rgb black (current node connects to another node)
		initiated BFS on black pixels untill we reach next node
		record relation between current and reached node
		return to point where we stopped and continue BFS
		if no more pixels to be discovered, break and continue iterating through rest of image mat
'''
