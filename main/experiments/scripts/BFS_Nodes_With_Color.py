import cv2 as cv
from collections import deque

#CONSTANTS

COLORS_BGR = {"red":(0, 0, 255),
    "green":(0, 255, 0),
    "purple":(240, 32, 160),
    "brown":(42, 42, 165),
    "pink":(203, 192, 255),
    "yellow":(0, 255, 255),
    "white":(255, 255, 255),
    "black":(0, 0, 0),
    "blue":(255, 0, 0)}

COLORS_DICT_BGR = {(0, 0, 255):("red", "A"),
    (0, 255, 0):("green", "G"),
    (240, 32, 160):("purple", "C"),
    (42, 42, 165):("brown", "D"),
    (203, 192, 255):("pink", "E"),
    (0, 255, 255):("yellow", "F"),
    (255, 255, 255):("white", "W"),
    (0, 0, 0):("black", "BL"),
    (255, 0, 0):("blue", "B")}


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

adjacency_list = {}

visited_pixels_set = set()

color_checker = {}

def vertice_edge_finder(filepath):
	image = cv.imread(filepath)
	for row in range(image.shape[0]):
		for col in range(image.shape[1]):
			bgr = tuple(image[row][col])
			if bgr in COLORS_DICT_BGR and bgr != WHITE and bgr != BLACK and COLORS_DICT_BGR[bgr][1] not in adjacency_list:
				#WE FOUND A NODE
				current_color = COLORS_DICT_BGR[bgr][0]
				adjacency_list[COLORS_DICT_BGR[bgr][1]] = {}
				#FIND ADJACENT NODE
				adjacent_colors = BFS((row, col), current_color, image)
				#CHECK IF WE FOUND ANY ADJACENT NODES
				if len(adjacent_colors) > 0:
					for nodes in adjacent_colors:
						adjacency_list[COLORS_DICT_BGR[bgr][1]][COLORS_DICT_BGR[tuple(nodes)][1]] = None
	print("COMPLETED")


def BFS(location, color, image):
	adjacent_nodes = []
	queue = deque([location])
	while queue:
		#REALISTICLY NEED TO CHECK FOR OUT OF BOUNDS BUT GRAPHVIZ IMAGES GIVES GOOD ENOUGH BUFFER BETWEEN NODES AND BOUNDARY OF IMAGE 
		curr = queue.popleft()
		if curr in visited_pixels_set:
			continue
		visited_pixels_set.add(curr)
		#CHECK SQUARE 3*3 TO SEE IF BLACK LINE IS PRESENT
		for row in range(curr[0]-2, curr[0]+3):
			for col in range(curr[1]-2, curr[1]+3):
				if tuple(image[row][col]) == BLACK and tuple(image[row][col]) not in visited_pixels_set:
					appended_node = False
					#START BFS TO FIND WHAT NODE BLACK LINE CONNECTS TO
					black_line_queue = deque([(row,col)])
					while black_line_queue:
						curr_black = black_line_queue.popleft()
						if curr_black in visited_pixels_set:
							continue
						visited_pixels_set.add(curr_black)
					
						#LOOKING AT SQUARE 3*3 TO SEE IF WE HAVE FOUND ANOTHER NODE		
						for black_row in range(curr_black[0]-2, curr_black[0]+3):
							for black_col in range(curr_black[1]-2, curr_black[1]+3):
								curr_pixel = tuple(image[black_row][black_col])
								if curr_pixel in COLORS_DICT_BGR and curr_pixel != BLACK and curr_pixel != WHITE and curr_pixel != COLORS_BGR[color]:
									adjacent_nodes.append(image[black_row][black_col])
									appended_node = True
									break
								elif curr_pixel == BLACK and (black_row, black_col) not in visited_pixels_set:
									black_line_queue.append((black_row, black_col))
						if appended_node:
							break
		#CONTINUE BFS
		for node_row in range(curr[0]-2, curr[0]+3):
			for node_col in range(curr[1]-2, curr[1]+3):
				if tuple(image[node_row][node_col]) in COLORS_DICT_BGR:
					if COLORS_DICT_BGR[tuple(image[node_row][node_col])][0] == color and (node_row, node_col) not in visited_pixels_set:
						queue.append((node_row, node_col))
	print(adjacent_nodes)
	return adjacent_nodes		
	

if __name__ == "__main__":
	print("STARTING")
	#TEST CASE
	for image in range(1, 8):
		filepath = f"/Users/warrenwilliams/Documents/School/UCSC Extension/Quarter 3/mlproject/graphviz_images/graphviz_find_colors_processed{image}.png"
		adjacency_list = {}
		visited_pixels_set = set()
		color_checker = {}
		vertice_edge_finder(filepath)
		print(f"WE FOUND NODES IN {image} WITH THIS RELATIONSHIP: ", adjacency_list)
	print("FINISHED") 
