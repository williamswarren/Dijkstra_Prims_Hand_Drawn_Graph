from graph_processing import *

class Graph_Manager():
	def __init__(self, file):
		self.graph_object = Graph_Processing(file)

	def show_original_image(self):
		self.graph_object.display_original()

	def show_processed_image(self):
		self.graph_object.display_processed()

	def process_graph(self):
		self.graph_object.process()
		self.graph_object.create_bound_box_weights()

	def update_weights(self):
		self.graph_object.update_weights()

	def compute_sp_mst(self):
		self.graph_object.get_sp()
		self.graph_object.get_mst()

	def create_graphviz(self):
		self.graph_object.create_graphviz_no_weights()
		self.graph_object.create_graphviz_with_weights()
		self.graph_object.create_graphviz_sp()
		self.graph_object.create_graphviz_mst()

	def save_images(self):
		self.graph_object.save_graphs()
