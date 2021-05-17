import cv2 as cv
import graphviz
import numpy as np
import copy
import heapq
from collections import deque

class Graph_Processing(cv, graphviz, deque, np, copy, heapq):
	def __init__(self, file):
		self.original_image = cv.imread(file)
		self.processed_image = None
		self.colors_set_bgr = {(0, 0, 255),
            (0, 255, 0),
            (240, 32, 160),
            (42, 42, 165),
            (203, 192, 255),
            (0, 255, 255),
            (255, 0, 0)}
		self.COLORS_DICT =  "A":"red",
			"G":"green",
			"C":"purple",
			"D":"brown",
			"P":"pink",
			"F":"yellow",
			"W":"white",
			"BL":black",
			"B":"blue"}
		self.adjacency_list = {}
		self.sp = None
		self.mst = None
		self.graphviz = Graph("Processed Graph", format="png")
	
	def display_original(self):
		cv.imshow("Original Image", self.original_image)
		cv.waitKey(0)
		cv.destroyAllWindows()

	def display_processed(self):	
		cv.imshow("Processed Image", self.processed_image)
		cv.waitKey(0)
		cv.destroyAllWindows()

	def update_weights(self):
		for nodes in self.adjacency_list.keys():
			if self.adjacency_list[nodes] != None:
				for edges in self.adjacency_list[nodes]:
					weight = input(f"Please give me the weight from nodes: {nodes} -> {edges} ")
					#Should type check
					self.adjacency_list[nodes][edges] = weight
	
	def create_graphviz_no_weights(self):
		if self.adjacency_list > 0:
			for nodes in self.adjacency_list.keys():
				self.graphviz.node(nodes, color=self.COLORS_DICT[nodes])

			for nodes in self.adjacency_list.keys():
				if self.adjacency_list[nodes] != None:
					for edges in self.adjacency_list[nodes]:
						self.graphviz.edge(nodes, edges)

	def create_graphviz_with_weights(self):
		if self.adjacency_list > 0:
			for nodes in self.adjacency_list.keys():
				self.graphviz.node(nodes, color=self.COLORS_DICT[nodes])

			for nodes in self.adjacency_list.keys():
				if self.adjacency_list[nodes] != None:
					for edges in self.adjacency_list[nodes]:
						self.graphviz.edge(nodes, edges, label=f"self.adjacency_list[nodes][edges]")

	
	
	def create_graphviz_sp(self):
		if self.adjacency_list > 0:
			for nodes in self.adjacency_list.keys():
				self.graphviz.node(nodes, color=self.COLORS_DICT[nodes])

			for nodes in self.adjacency_list.keys():
				if self.adjacency_list[nodes] != None:
					for edges in self.adjacency_list[nodes]:
						self.graphviz.edge(nodes, edges, label=f"self.adjacency_list[nodes][edges]")

	
	def create_graphviz_mst(self):
		if self.adjacency_list > 0:
			for nodes in self.adjacency_list.keys():
				self.graphviz.node(nodes, color=self.COLORS_DICT[nodes])

			for nodes in self.adjacency_list.keys():
				if self.adjacency_list[nodes] != None:
					for edges in self.adjacency_list[nodes]:
						self.graphviz.edge(nodes, edges, label=f"self.adjacency_list[nodes][edges]")
	
	
	def save_graphs(self):
		self.graphviz.render("./processed-graph.gv" ,view=False)
		cv.imwrite("processed-image.png", self.processed_image)


	def get_mst(self):
		#DO MST

	def get_sp(self):
		#DO SP

	def get_adjacency_list:
		graph_copy = copy.deepcopy(self.adjacency_list)
		return graph_copy
		
	
	
	def process(self):

		def binarize(self):
        	gray = cv.cvtColor(self.original_image, cv.COLOR_BGR2GRAY)
        	th, threshed = cv.threshold(gray, 100, 255, cv.THRESH_OTSU|cv.THRESH_BINARY_INV)
        	self.processed_image = cv.morphologyEx(threshed, cv.MORPH_OPEN, np.ones((2,2)))

    	def circles(self):
        	gray = cv.cvtColor(self.original_image, cv.COLOR_BGR2GRAY)
        	img = cv.medianBlur(gray,5)
        	#cimg = cv.cvtColor(img,cv2.COLOR_GRAY2BGR)

        	circles = cv.HoughCircles(img,cv.HOUGH_GRADIENT,1,100, param1=80,param2=40,minRadius=100,maxRadius=550)

        	circles = np.uint16(np.around(circles))
        	for i in circles[0,:]:
            	# get colors and draw the outer circle
            	if len(self.colors_set_bgr) >= 1:
                	color = self.colors_set_bgr.pop()
                	cv.circle(self.processed_image,(i[0],i[1]),i[2],color,2)
            	else:
                	cv.circle(self.processed_image,(i[0],i[1]),i[2],(255, 255, 200),2)

            	# draw the center of the circle
            	#cv.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
			

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

		def vertice_edge_finder():
			image = self.processed_image
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
			self.adjacency_list = adjacency_list		
				
				
		def BFS(location, color, image):
			adjacent_nodes = []
			queue = deque([location])
			while queue:
				#REALISTICLY NEED TO CHECK FOR OUT OF BOUNDS BUT GRAPHVIZ IMAGES GIVES GOOD ENOUGH BUFFER BETWEEN NODES AND BOUNDARY OF IMAGE
				curr = queue.popleft()
				if curr in visited_pixels_set:
					continue
				visited_pixels_set.add(curr)
				#CHECK SQUARE 3*3 TO SEE IF WHITE LINE IS PRESENT
				for row in range(curr[0]-2, curr[0]+3):
					for col in range(curr[1]-2, curr[1]+3):
						if tuple(image[row][col]) == WHITE and tuple(image[row][col]) not in visited_pixels_set:
							appended_node = False
							#START BFS TO FIND WHAT NODE WHITE LINE CONNECTS TO
							white_line_queue = deque([(row,col)])
							while white_line_queue:
								curr_white = white_line_queue.popleft()
								if curr_white in visited_pixels_set:
									continue
								visited_pixels_set.add(curr_white)

								#LOOKING AT SQUARE 3*3 TO SEE IF WE HAVE FOUND ANOTHER NODE
								for white_row in range(curr_white[0]-2, curr_white[0]+3):
									for white_col in range(curr_white[1]-2, curr_white[1]+3):
										curr_pixel = tuple(image[white_row][white_col])
										if curr_pixel in COLORS_DICT_BGR and curr_pixel != WHITE and curr_pixel != BLACK and curr_pixel != COLORS_BGR[color]:
											adjacent_nodes.append(image[white_row][white_col])
											appended_node = True
											break
										elif curr_pixel == WHITE and (white_row, white_col) not in visited_pixels_set:
											white_line_queue.append((white_row, white_col))
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

	
        binarize()
        circles()
        vertice_edge_finder()		
			
