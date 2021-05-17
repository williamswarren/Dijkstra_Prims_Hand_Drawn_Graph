import graph_processing

class Graph_Manager():
	def __init__(self, file):
		self.graph_object = self.Graph_Processing(file)

	def show_original_image(self):
		self.graph_object.display_original()

	def show_processed_image(self):
		self.graph_object.display_processed()

	def process_graph(self):
		self.graph_object.process()

	def show_sp(self):
		self.graph_object.display_sp()

	def show_mst(self):
		self.graph_object.display_mst()

	def get_adj_list(self):
		self.graph_object.get_adjacency_list()

	def save_images(self):
		self.graph_object.save_graphs()
