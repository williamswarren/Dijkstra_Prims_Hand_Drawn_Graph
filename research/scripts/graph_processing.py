import cv2 as cv
from graphviz import Graph
import numpy as np
import copy
import heapq
from collections import deque

class Graph_Processing():
	def __init__(self, file):
		self.original_image = cv.imread(file)
		self.processed_image = None
		self.processed_image_weights = None
		self.boundary_boxes_digits = None
		self.colors_bgr = [(0, 0, 255),
            (0, 255, 0),
            (240, 32, 160),
            (42, 42, 165),
            (203, 192, 255),
            (0, 255, 255),
            (255, 0, 0)]
		self.COLORS_DICT =  {"A":"red",
			"G":"green",
			"C":"purple",
			"D":"brown",
			"E":"pink",
			"F":"yellow",
			"W":"white",
			"BL":"black",
			"B":"blue"}
		self.adjacency_list = {}
		self.sp = None
		self.mst = None
		self.graphviz_original = Graph("Processed Graph", format="png")
		self.graphviz_weights = Graph("Processed Weighted Graph", format="png")
		self.graphviz_sp = Graph("Shortest Path Graph", format="png")
		self.graphviz_mst = Graph("MST Graph", format="png")
	
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
					weight = int(input(f"Please give me the weight from nodes: {self.COLORS_DICT[nodes]} -> {self.COLORS_DICT[edges]} "))
					#Should type check
					self.adjacency_list[nodes][edges] = weight

	def create_bound_box_weights(self):
		img = self.original_image
		gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

		# (2) threshold-inv and morph-open 
		th, threshed = cv.threshold(gray, 100, 255, cv.THRESH_OTSU|cv.THRESH_BINARY_INV)
		morphed = cv.morphologyEx(threshed, cv.MORPH_OPEN, np.ones((2,2)))
		# (3) find and filter contours, then draw on src 
		cnts = cv.findContours(morphed, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)[-2]


		nh, nw = img.shape[:2]
		#print(cnts)
		self.boundary_boxes_digits = cnts
		for cnt in cnts:
			x,y,w,h = bbox = cv.boundingRect(cnt)
			#print(bbox)
			#print("height", h)
			if 15 < h < 100 and 15 < w < 100:
				cv.rectangle(img, (x,y), (x+w, y+h), (255, 0, 255), 1, cv.LINE_AA)
				#print(bbox)
		self.processed_image_weights = img


	
	def create_graphviz_no_weights(self):
		if len(self.adjacency_list) > 0:
			for nodes in self.adjacency_list.keys():
				self.graphviz_original.node(nodes, color=self.COLORS_DICT[nodes])

			for nodes in self.adjacency_list.keys():
				if self.adjacency_list[nodes] != None:
					for edges in self.adjacency_list[nodes]:
						self.graphviz_original.edge(nodes, edges)

	def create_graphviz_with_weights(self):
		if len(self.adjacency_list) > 0:
			for nodes in self.adjacency_list.keys():
				self.graphviz_weights.node(nodes, color=self.COLORS_DICT[nodes])

			for nodes in self.adjacency_list.keys():
				if self.adjacency_list[nodes] != None:
					for edges in self.adjacency_list[nodes]:
						weight = f"{self.adjacency_list[nodes][edges]}"
						self.graphviz_weights.edge(nodes, edges, label= weight)

	
	#USE PYGRAPHVIZ	
	def create_graphviz_sp(self):
		count = 0
		if self.sp != None:
			self.graphviz_sp = copy.deepcopy(self.graphviz_weights)
			'''		
			for nodes in self.adjacency_list.keys():
				self.graphviz_sp.node(nodes, color=self.COLORS_DICT[nodes])
			'''

			for nodes, edges in self.sp.items():
				if count == 0:
					count += 1
					continue
				weight = f"{edges[0]}"
				self.graphviz_sp.edge(edges[2], nodes, label= weight, color="red")



	#USE PYGRAPHVIZ
	def create_graphviz_mst(self):
		if self.mst != None:
			self.graphviz_mst = copy.deepcopy(self.graphviz_weights)
			'''
			for nodes in self.adjacency_list.keys():
				self.graphviz_mst.node(nodes, color=self.COLORS_DICT[nodes])
			'''

			for nodes in self.mst:
				weight = f"{nodes[0]}"
				self.graphviz_mst.edge(nodes[1], nodes[2], label= weight, color="red")
	
	
	def save_graphs(self):
		self.graphviz_original.render("./processed-graph.gv" ,view=False)
		self.graphviz_weights.render("./processed-graph-weights.gv" ,view=False)
		self.graphviz_sp.render("./processed-graph-sp.gv" ,view=False)
		self.graphviz_mst.render("./processed-graph-mst.gv" ,view=False)
		cv.imwrite("processed-image.png", self.processed_image)
		cv.imwrite("processed-image-weights.png", self.processed_image_weights)


	def get_mst(self):
		def helper(current_node):
			for item in mst_dic_list[current_node[1]]:
				heapq.heappush(mst_heap, item)
				current_node = heapq.heappop(mst_heap)
			while len(mst) < len(visited_nodes)-1:
				#print('MST', mst)
				#print("Heap", mst_heap)
				#print(current_node)
				temp_node = None
				visited_nodes[current_node[1]] = True
				visited_nodes[current_node[2]] = True
				mst.append(current_node)
				if len(mst) == len(visited_nodes)-1:
					break

				for items in mst_dic_list[current_node[2]]:
					if visited_nodes[items[2]] != True: 
						heapq.heappush(mst_heap,items)

				while current_node[2] not in mst_dic_list or visited_nodes[current_node[2]] == True:
					temp_node = heapq.heappop(mst_heap)
					current_node = temp_node

				if temp_node:
					current_node = temp_node
				else:
					current_node = heapq.heappop(mst_heap)			


		visited_nodes = {key:False for key in self.adjacency_list.keys()}
		mst = []
		mst_heap = []
		heapq.heapify(mst_heap)
		mst_dic_list = {}

		#formatting
		
		adjacent_list = copy.deepcopy(self.adjacency_list)
		for node in adjacent_list:
			for edges in adjacent_list[node]:
				if node not in adjacent_list[edges]:
					adjacent_list[edges][node] = adjacent_list[node][edges]


		for key, value in adjacent_list.items():
			for k,v in value.items():
				if key not in mst_dic_list:
					mst_dic_list[key] = []
					mst_dic_list[key].append([v, key, k])
				else:
					mst_dic_list[key].append([v, key, k])

		current_node = mst_dic_list["A"][0]
		helper(current_node)
		self.mst = mst
		

	def get_sp(self):
		heap_pos_list = [[float('inf'), key, 'Prev'] for key in self.adjacency_list.keys()]
		heap_pos_list[0][0] = 0
		heap_pos_dic = {tuples[1]:tuples for tuples in heap_pos_list}
		heap = []
		heapq.heapify(heap)
		for item in heap_pos_dic.values():
			heapq.heappush(heap, item)
		visited = {key:False for key in heap_pos_dic.keys()}
		while len(heap) > 0:
			current_node = heapq.heappop(heap)
			if visited[current_node[1]] != True:
				visited[current_node[1]] = True
				for node, distance in self.adjacency_list[current_node[1]].items():
					if current_node[0] + distance < heap_pos_dic[node][0]:
						heap_pos_dic[node][0] = current_node[0] + distance
						heap_pos_dic[node][2] = current_node[1]
						#print(heap)
						heapq.heapify(heap)
						#print(heap)		
		self.sp = heap_pos_dic

	def get_adjacency_list(self):
		graph_copy = copy.deepcopy(self.adjacency_list)
		return graph_copy
		
	
	
	def process(self):

		def binarize():
			gray = cv.cvtColor(self.original_image, cv.COLOR_BGR2GRAY)
			th, threshed = cv.threshold(gray, 100, 255, cv.THRESH_OTSU|cv.THRESH_BINARY_INV)
			temp = cv.morphologyEx(threshed, cv.MORPH_OPEN, np.ones((2,2)))
			self.processed_image = cv.merge([temp,temp,temp])

		def circles():
			gray = cv.cvtColor(self.original_image, cv.COLOR_BGR2GRAY)
			img = cv.medianBlur(gray,5)
			#cimg = cv.cvtColor(img,cv2.COLOR_GRAY2BGR)

			circles = cv.HoughCircles(img,cv.HOUGH_GRADIENT,1,100, param1=80,param2=40,minRadius=100,maxRadius=300)

			circles = np.uint16(np.around(circles))
			for i in circles[0,:]:
				# get colors and draw the outer circle
				if len(self.colors_bgr) >= 1:
					color = self.colors_bgr.pop(0)
					cv.circle(self.processed_image,(i[0],i[1]),i[2],color,6)
				else:
					cv.circle(self.processed_image,(i[0],i[1]),i[2],(255, 255, 200),6)

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
					print(row, col)
					bgr = tuple(image[row][col])
					#print(bgr) 
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
			#print("COMPLETED")
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
			#print(adjacent_nodes)
			return adjacent_nodes

	
		binarize()
		circles()
		vertice_edge_finder()		
			
