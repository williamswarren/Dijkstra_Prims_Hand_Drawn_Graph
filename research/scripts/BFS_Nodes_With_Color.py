import cv2 as cv
from collections import deque

#CONSTANTS

COLORS_BGR = {"red":(0, 0, 255),
	"green":(0, 255, 0),
	"purple":(240, 32, 160),
	"orange":(0, 165, 255),
	"pink":(203, 192, 255),
	"yellow":(0, 255, 255),
	"green":(0, 255, 0),
	"white":(255, 255, 255),
	"black":(0, 0, 0),
	"blue":(255, 0, 0)}


COLORS_SET_BGR = {(0, 0, 255),
	(0, 255, 0),
	(240, 32, 160),
	(0, 165, 255),
	(203, 192, 255),
	(0, 255, 255),
	(0, 255, 0),
	(255, 255, 255),
	(0, 0, 0),
	(255, 0, 0)}


LETTERS_MAPPING = {"red":"A",
		"blue":"B",
		"purple":"C",
		"orange":"D",
		"pink":"E",
		"yellow":"F",
		"green":"G"}

adjacency_list = {}

visited_pixels_set = set()

def vertice_edge_finder(filepath):
	image = cv.imread(filepath)
	for i in range(image.shape[0]):
		for j in range(image.shape[1]):
			#print("INSIDE MAIN IMAGE LOOP")
			if (i, j) in visited_pixels_set:
				continue
			visited_pixels_set.add((i, j))
			#WE FOUND A NODE
			if tuple(image[i][j]) in COLORS_SET_BGR and (tuple(image[i][j]) != COLORS_BGR["white"] and tuple(image[i][j]) != COLORS_BGR["black"]):
				for color in COLORS_BGR.keys():
					if COLORS_BGR[color] == tuple(image[i][j]) and LETTERS_MAPPING[color] not in adjacency_list:
						#COLOR/LETTER NODE FOUND
						current_color = color
						adjacency_list[LETTERS_MAPPING[current_color]] = {}
						#FIND ADJACENT NODE
						#print("FOUND NODE: ", current_color)
						adjacent_colors = BFS((i, j), current_color, image)
						#print("FOUND ADJACENT COLORS: ", adjacent_colors)
						if len(adjacent_colors) > 0:
							for nodes in adjacent_colors:
								for key in COLORS_BGR.keys():
									if COLORS_BGR[key] == tuple(nodes):
										adjacency_list[LETTERS_MAPPING[current_color]][LETTERS_MAPPING[key]] = None
						else:
							continue

	print("COMPLETED")


def BFS(location, color, image):
	#print("INSIDE BFS LOOP")
	adjacent_nodes = []
	queue = deque([location])
	first_time = True
	while queue:
		#REALISTICLY NEED TO CHECK FOR OUT OF BOUNDS BUT GRAPHVIZ IMAGES GIVES GOOD ENOUGH BUFFER BETWEEN NODES AND BOUNDARY OF IMAGE 
		curr = queue.popleft()
		if curr in visited_pixels_set and not first_time:
			continue
		visited_pixels_set.add(curr)
		first_time = False
		#CHECK SQUARE 6*6 TO SEE IF BLACK LINE IS PRESENT
		for k in range(curr[0]-3, curr[0]+3):
			for l in range(curr[1]-3, curr[1]+9):
				#print("INSIDE COLOR NODE AND CHECKING FOR BLACK LINE: ", color)
				if tuple(image[k][l]) == COLORS_BGR["black"] and tuple(image[k][l]) not in visited_pixels_set:
					appended_node = False
					#START BFS TO FIND NODE WHAT BLACK LINE CONNECTS TO
					#print("FOUND A BLACK LINE PIXEL******************************* at : ", (k,l))
					black_line_queue = deque([(k,l)])
					
					while black_line_queue:
						curr_black = black_line_queue.popleft()
						if curr_black in visited_pixels_set:
							#print("CURRENT PIXEL ALREADY VISITED")
							continue
						visited_pixels_set.add(curr_black)
					
						#LOOKING AT SQUARE 6*6 TO SEE IF WE HAVE FOUND ANOTHER NODE		
						for m in range(curr_black[0]+1, curr_black[0]+4):
							for n in range(curr_black[1]-3, curr_black[1]+3):
								if tuple(image[m][n]) in COLORS_SET_BGR and (tuple(image[m][n])!= COLORS_BGR['black'] and tuple(image[m][n]) != COLORS_BGR['white'] and tuple(image[m][n]) != COLORS_BGR[color]):
									#print("FOUND AN ADJACENT NODE WITH COLOR: ", image[m][n])
									adjacent_nodes.append(image[m][n])
									appended_node = True
									break
							if appended_node:
								break
						#print("BLACK LINE QUEUE: ", black_line_queue)
						#SUM CHECK BECAUSE SOME PIXELS ARE NOT QUITE (0, 0, 0)	
						if (tuple(image[curr_black[0]-1][curr_black[1]]) == COLORS_BGR['black'] or sum(tuple(image[curr_black[0]-1][curr_black[1]])) < 30) and (curr_black[0]-1, curr_black[1]) not in visited_pixels_set:
							black_line_queue.append((curr_black[0]-1, curr_black[1]))
		
						if (tuple(image[curr_black[0]+1][curr_black[1]]) == COLORS_BGR['black'] or sum(tuple(image[curr_black[0]+1][curr_black[1]])) < 30) and (curr_black[0]+1, curr_black[1]) not in visited_pixels_set:
							black_line_queue.append((curr_black[0]+1, curr_black[1]))

						if (tuple(image[curr_black[0]][curr_black[1]+1]) == COLORS_BGR['black'] or sum(tuple(image[curr_black[0]][curr_black[1]+1])) < 30) and (curr_black[0], curr_black[1]+1) not in visited_pixels_set:
							black_line_queue.append((curr_black[0], curr_black[1]+1))

						if (tuple(image[curr_black[0]][curr_black[1]-1]) == COLORS_BGR['black'] or sum(tuple(image[curr_black[0]][curr_black[1]-1])) < 30) and (curr_black[0], curr_black[1]-1) not in visited_pixels_set:
							black_line_queue.append((curr_black[0], curr_black[1]-1))
						



		#print("DID NOT FIND A BLACK NODE, CONTINUE BFS")	
		#IF WE DID NOT FIND A BLACK PIXEL IN 6*6 MATRIX WE CONTINUE THE BFS ON THE NODE
		#MANY IF'S BECAUSE THE TRANSITION FROM 1 COLOR PIXEL TO THE NEXT IS NOT LINEAR AND GRAPHVIZ GIVES MANY SHADES OF E.G. A RED PIXEL WHICH IS VERY ANNOYING
		
		if tuple(image[curr[0]-1][curr[1]]) == COLORS_BGR[color] and (curr[0]-1, curr[1]) not in visited_pixels_set:
			queue.append((curr[0]-1, curr[1]))
		
		
		if tuple(image[curr[0]+1][curr[1]]) == COLORS_BGR[color] and (curr[0]+1, curr[1]) not in visited_pixels_set:
			queue.append((curr[0]+1, curr[1]))

		
		if tuple(image[curr[0]][curr[1]+1]) == COLORS_BGR[color] and (curr[0], curr[1]+1) not in visited_pixels_set:
			queue.append((curr[0], curr[1]+1))

		
		if tuple(image[curr[0]][curr[1]-1]) == COLORS_BGR[color] and (curr[0], curr[1]-1) not in visited_pixels_set:
			queue.append((curr[0], curr[1]-1))

		
		if tuple(image[curr[0]-2][curr[1]]) == COLORS_BGR[color] and (curr[0]-2, curr[1]) not in visited_pixels_set:
			queue.append((curr[0]-2, curr[1]))
		
		
		if tuple(image[curr[0]+1][curr[1]-4]) == COLORS_BGR[color] and (curr[0]+2, curr[1]) not in visited_pixels_set:
			queue.append((curr[0]+2, curr[1]))

		
		if tuple(image[curr[0]+1][curr[1]+4]) == COLORS_BGR[color] and (curr[0], curr[1]+2) not in visited_pixels_set:
			queue.append((curr[0], curr[1]+2))

		
		if tuple(image[curr[0]][curr[1]-2]) == COLORS_BGR[color] and (curr[0], curr[1]-2) not in visited_pixels_set:
			queue.append((curr[0], curr[1]-2))

	return adjacent_nodes		
	

if __name__ == "__main__":
	print("STARTING")
	filepath = "../../graphviz_images/Nodes_With_Color1.png"
	vertice_edge_finder(filepath)
	print("WE FOUND NODES WITH THIS RELATIONSHIP: ", adjacency_list)
	print("FINISHED") 
