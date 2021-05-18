from graph_manager import *
from graph_processing import *
import sys


def main(file_path):
	print("PROCESSING")
	manager = Graph_Manager(file_path)
	manager.show_original_image()
	manager.process_graph()
	manager.show_processed_image()
	manager.update_weights()
	manager.compute_sp_mst()
	manager.create_graphviz()
	manager.save_images()
	del manager

if __name__ == "__main__":
	print("STARTING")
	file_path = str(sys.argv[1])
	main(file_path)
	print("FINISHED")
