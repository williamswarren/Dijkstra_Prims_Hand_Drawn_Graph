import cv2 as cv
from collections import deque

#CONSTANTS
'''
COLORS_BGR = {"red":(0, 0, 255),
	"green":(0, 255, 0),
	"lightseagreen":(92, 144, 0),
	"deepskyblue":(255, 201, 0),
	"skyblue":(255, 251, 0),
	"yellow":(0, 255, 255),
	"white":(255, 255, 255),
	"black":(0, 0, 0),
	"blue":(255, 0, 0)}
'''

COLORS_BGR = {"red":(0, 0, 255),
    "green":(0, 255, 0),
    "purple":(240, 32, 160),
    "brown":(42, 42, 165),
    "pink":(203, 192, 255),
    "yellow":(0, 255, 255),
    "white":(255, 255, 255),
    "black":(0, 0, 0),
    "blue":(255, 0, 0)}




COLORS_SET_BGR = {(0, 0, 255),
	(0, 255, 0),
	(92, 144, 0),
	(255, 201, 0),
	(255, 251, 0),
	(0, 255, 255),
	(255, 255, 255),
	(0, 0, 0),
	(255, 0, 0)}

'''
COLORS_DICT_BGR = {(0, 0, 255):("red", "A"),
	(0, 255, 0):("green", "G"),
	(92, 144, 0):("lightseagreen", "C"),
	(255, 201, 0):("deepskyblue", "D"),
	(255, 251, 0):("skyblue", "E"),
	(0, 255, 255):("yellow", "F"),
	(255, 255, 255):("white", "W"),
	(0, 0, 0):("black", "BL"),
	(255, 0, 0):("blue", "B")}
'''
COLORS_DICT_BGR = {(0, 0, 255):("red", "A"),
    (0, 255, 0):("green", "G"),
    (240, 32, 160):("purple", "C"),
    (42, 42, 165):("brown", "D"),
    (203, 192, 255):("pink", "E"),
    (0, 255, 255):("yellow", "F"),
    (255, 255, 255):("white", "W"),
    (0, 0, 0):("black", "BL"),
    (255, 0, 0):("blue", "B")}



LETTERS_MAPPING = {"red":"A",
		"blue":"B",
		"lightseagreen":"C",
		"deepskyblue":"D",
		"skyblue":"E",
		"yellow":"F",
		"green":"G"}

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

adjacency_list = {}

visited_pixels_set = set()

color_checker = {}

def vertice_edge_finder(filepath):
	image = cv.imread(filepath)
	# XCR hkumar for wwililams: xrange always, you can google why.
	#
	# wwilliams: It's python3 probably
	for row in range(image.shape[0]):
		for col in range(image.shape[1]):
			#if tuple(image[i][j]) not in color_checker:
				#color_checker[tuple(image[i][j])] = 1
			#else:
				#color_checker[tuple(image[i][j])] += 1
			#print("INSIDE MAIN IMAGE LOOP")
			#if (i, j) in visited_pixels_set:
				#continue
			# CR hkumar for hkumar: I think we don't need to add the px to visited here, reason about it more. 
			#visited_pixels_set.add((i, j))
			#WE FOUND A NODE
			bgr = tuple(image[row][col])
			if bgr in COLORS_DICT_BGR and bgr != WHITE and bgr != BLACK and COLORS_DICT_BGR[bgr][1] not in adjacency_list:
				#for color in COLORS_BGR.keys():
				#if COLORS_DICT_BGR[bgr][1] not in adjacency_list:
				#COLOR/LETTER NODE FOUND
				current_color = COLORS_DICT_BGR[bgr][0]
				print(current_color, "current_color")
				adjacency_list[COLORS_DICT_BGR[bgr][1]] = {}
				#FIND ADJACENT NODE
				#print("FOUND NODE: ", current_color)
				adjacent_colors = BFS((row, col), current_color, image)
				print("FOUND ADJACENT COLORS: ", adjacent_colors)
				if len(adjacent_colors) > 0:
					for nodes in adjacent_colors:
						adjacency_list[COLORS_DICT_BGR[bgr][1]][COLORS_DICT_BGR[tuple(nodes)][1]] = None
						#for key in COLORS_BGR.keys():
							#if COLORS_BGR[key] == tuple(nodes):
								#adjacency_list[LETTERS_MAPPING[current_color]][LETTERS_MAPPING[key]] = None
						#else:
							#continue
			#visited_pixels_set.add((row, col))
	print("COMPLETED")


def BFS(location, color, image):
	#print("INSIDE BFS LOOP")
	adjacent_nodes = []
	queue = deque([location])
	#first_time = True
	while queue:
		#REALISTICLY NEED TO CHECK FOR OUT OF BOUNDS BUT GRAPHVIZ IMAGES GIVES GOOD ENOUGH BUFFER BETWEEN NODES AND BOUNDARY OF IMAGE 
		curr = queue.popleft()
		if curr in visited_pixels_set:
			continue
		visited_pixels_set.add(curr)
		#first_time = False
		#CHECK SQUARE 6*6 TO SEE IF BLACK LINE IS PRESENT
		#if any(tuple(image[curr[0]-1][curr[1]-1]),  tuple(image[curr[0]-1][curr[1]]), tuple(image[curr[0]-1][curr[1]+1]), tuple(image[curr[0]][curr[1]-1]), tuple(image[curr[0]][curr[1]+1]), tuple(image[curr[0]+1][curr[1]-1]), tuple(image[curr[0]+1][curr[1]]), tuple(image[curr[0]+1][curr[1]+1])) == BLACK:
		for row in range(curr[0]-2, curr[0]+3):
			for col in range(curr[1]-2, curr[1]+3):
				#print("INSIDE COLOR NODE AND CHECKING FOR BLACK LINE: ", color)
				if tuple(image[row][col]) == BLACK and tuple(image[row][col]) not in visited_pixels_set:
					appended_node = False
					#START BFS TO FIND NODE WHAT BLACK LINE CONNECTS TO
					#print("FOUND A BLACK LINE PIXEL******************************* at : ", (row,col))
					black_line_queue = deque([(row,col)])
					
					while black_line_queue:
						curr_black = black_line_queue.popleft()
						if curr_black in visited_pixels_set:
							#print("CURRENT PIXEL ALREADY VISITED")
							continue
						visited_pixels_set.add(curr_black)
					
						#LOOKING AT SQUARE 6*6 TO SEE IF WE HAVE FOUND ANOTHER NODE		
						for black_row in range(curr_black[0]-2, curr_black[0]+3):
							for black_col in range(curr_black[1]-2, curr_black[1]+3):
								curr_pixel = tuple(image[black_row][black_col])
								if curr_pixel in COLORS_DICT_BGR and curr_pixel != BLACK and curr_pixel != WHITE and curr_pixel != COLORS_BGR[color]:
									print("FOUND AN ADJACENT NODE WITH COLOR: ", image[black_row][black_col])
									adjacent_nodes.append(image[black_row][black_col])
									appended_node = True
									break
								elif curr_pixel == BLACK and (black_row, black_col) not in visited_pixels_set:
									black_line_queue.append((black_row, black_col))
						if appended_node:
							break
						#print("BLACK LINE QUEUE: ", black_line_queue)
						#SUM CHECK BECAUSE SOME PIXELS ARE NOT QUITE (0, 0, 0)
						'''	
						if (tuple(image[curr_black[0]-1][curr_black[1]]) == COLORS_BGR['black'] or sum(tuple(image[curr_black[0]-1][curr_black[1]])) < 30) and (curr_black[0]-1, curr_black[1]) not in visited_pixels_set:
							black_line_queue.append((curr_black[0]-1, curr_black[1]))
		
						if (tuple(image[curr_black[0]+1][curr_black[1]]) == COLORS_BGR['black'] or sum(tuple(image[curr_black[0]+1][curr_black[1]])) < 30) and (curr_black[0]+1, curr_black[1]) not in visited_pixels_set:
							black_line_queue.append((curr_black[0]+1, curr_black[1]))

						if (tuple(image[curr_black[0]][curr_black[1]+1]) == COLORS_BGR['black'] or sum(tuple(image[curr_black[0]][curr_black[1]+1])) < 30) and (curr_black[0], curr_black[1]+1) not in visited_pixels_set:
							black_line_queue.append((curr_black[0], curr_black[1]+1))

						if (tuple(image[curr_black[0]][curr_black[1]-1]) == COLORS_BGR['black'] or sum(tuple(image[curr_black[0]][curr_black[1]-1])) < 30) and (curr_black[0], curr_black[1]-1) not in visited_pixels_set:
							black_line_queue.append((curr_black[0], curr_black[1]-1))
						'''



		#print("DID NOT FIND A BLACK NODE, CONTINUE BFS")	
		#IF WE DID NOT FIND A BLACK PIXEL IN 6*6 MATRIX WE CONTINUE THE BFS ON THE NODE
		#MANY IF'S BECAUSE THE TRANSITION FROM 1 COLOR PIXEL TO THE NEXT IS NOT LINEAR AND GRAPHVIZ GIVES MANY SHADES OF E.G. A RED PIXEL WHICH IS VERY ANNOYING

		# CR hkumar for wwiliams: This seems really hacky and as you mentioned, annoying, any way to photoshop the graph to have the pixel structure we desire?
		for node_row in range(curr[0]-2, curr[0]+3):
			for node_col in range(curr[1]-2, curr[1]+3):
				if tuple(image[node_row][node_col]) in COLORS_DICT_BGR:
					#print(row, col)
					if COLORS_DICT_BGR[tuple(image[node_row][node_col])][0] == color and (node_row, node_col) not in visited_pixels_set:
						queue.append((node_row, node_col))
		'''
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
		'''
	print(adjacent_nodes)
	return adjacent_nodes		
	

if __name__ == "__main__":
	print("STARTING")
	for image in range(1, 8):
		filepath = f"/Users/warrenwilliams/Documents/School/UCSC Extension/Quarter 3/mlproject/graphviz_images/graphviz_find_colors_processed{image}.png"
		adjacency_list = {}
		visited_pixels_set = set()
		color_checker = {}
		vertice_edge_finder(filepath)
		print(f"WE FOUND NODES IN {image} WITH THIS RELATIONSHIP: ", adjacency_list)
	# CR hkumar for wwilliams: We have a library to print graphs, 
	# In addition to the above print statement, 
	# why don't you also create an image of [adjacency_list] and save it in say [result_graph.png]
	#for key, value in color_checker.items():
		#if value >= 100:
			#print(key, value)
	print("FINISHED") 
