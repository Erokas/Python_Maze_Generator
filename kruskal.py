from common_functions import possible_choices, display_tensor
import random
import numpy as np


def update_maze_tensor_for_kruskal(maze_tensor, maze_canvas):
	set_num = 6

	for y in range(maze_canvas.shape[0]):
		for x in range(maze_canvas.shape[1]):
			maze_tensor[y, x, 4] = set_num
			set_num = set_num + 1

	return maze_tensor


def change_all_set_tiles(maze_tensor, from_, to):
	maze_tensor[maze_tensor == from_] = to
	return maze_tensor


def solve_maze_kruskal(root, maze_tensor, maze_canvas, Canvas_param):
	#prevent other buttons from working
	Canvas_param.displaying_maze = True

	# prepare tensor for kruskal
	Canvas_param.maze_tensor = update_maze_tensor_for_kruskal(Canvas_param.maze_tensor, Canvas_param)
	# run while there is more than one set
	while not np.all(Canvas_param.maze_tensor[:, :, 4] == Canvas_param.maze_tensor[0, 0, 4]):
		for y in range(Canvas_param.shape[0]):
			for x in range(Canvas_param.shape[1]):

				#test if user aborted maze generation
				if Canvas_param.abort_generation == True:
					#terminate maze generation
					#give back control to user
					Canvas_param.displaying_maze = False
					return maze_tensor

				tile_choices = []
				tile_choices = possible_choices(Canvas_param.maze_tensor, (y, x), "kruskal")
				# set to zero if tile has no choices to skip sorted tiles
				if len(tile_choices) == 0:
					Canvas_param.maze_tensor[y, x, 5] = 0

				else:
					move_direction = random.choices(tile_choices)
					# FIX SO THERE IS ONLY ONE MERGE FUNCTION CALL
					if move_direction[0] == 0:
						Canvas_param.maze_tensor[y, x, 0] = 0
						Canvas_param.maze_tensor[y - 1, x, 2] = 0

						# merge sets
						Canvas_param.maze_tensor = change_all_set_tiles(
							Canvas_param.maze_tensor, Canvas_param.maze_tensor[y - 1, x, 4], Canvas_param.maze_tensor[y, x, 4])
					if move_direction[0] == 1:
						Canvas_param.maze_tensor[y, x, 1] = 0
						Canvas_param.maze_tensor[y, x + 1, 3] = 0

						# merge sets
						Canvas_param.maze_tensor = change_all_set_tiles(
							Canvas_param.maze_tensor, Canvas_param.maze_tensor[y, x + 1, 4], Canvas_param.maze_tensor[y, x, 4])
					if move_direction[0] == 2:
						Canvas_param.maze_tensor[y, x, 2] = 0
						Canvas_param.maze_tensor[y + 1, x, 0] = 0

						# merge sets
						Canvas_param.maze_tensor = change_all_set_tiles(
							Canvas_param.maze_tensor, Canvas_param.maze_tensor[y + 1, x, 4], Canvas_param.maze_tensor[y, x, 4])
					if move_direction[0] == 3:
						Canvas_param.maze_tensor[y, x, 3] = 0
						Canvas_param.maze_tensor[y, x - 1, 1] = 0

						# merge sets
						Canvas_param.maze_tensor = change_all_set_tiles(
							Canvas_param.maze_tensor, Canvas_param.maze_tensor[y, x - 1, 4], Canvas_param.maze_tensor[y, x, 4])

				if Canvas_param.display_process:
					display_tensor(root, maze_canvas, Canvas_param)

	display_tensor(root, maze_canvas, Canvas_param)

	#give back control to user
	Canvas_param.displaying_maze = False
	return maze_tensor
