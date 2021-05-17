import graph_manager
import graph_processing
import sys


main():
	print("PROCESSING")
	file_path = str(sys.argv[1])
	manager = Graph_Manager(file_path)
	manager.show_original_image()
	manager.process_graph()
	manager.show_processed_image()
	manager.compute_sp_mst()
	manager.save_images()
	del manager

if __name__ == "__main__":
	print("STARTING")
	main()
	print(FINISHED)
