from common_functions import display_tensor, possible_choices
import random


def solve_maze_deep_search(root, maze_tensor, cord, end_cord, maze_canvas, Canvas_param):
	#prevent other buttons from working
	Canvas_param.displaying_maze = True

	maze_stack = [cord]

	# set start coordinate to maze start
	Canvas_param.maze_tensor[cord[0], cord[1], 4] = 3

	while len(maze_stack) > 0:
		choice_list = possible_choices(Canvas_param.maze_tensor, cord, "deep")

		if len(choice_list) == 0 or cord == end_cord:
			cord = maze_stack.pop()
		else:
			move_direction = random.choices(choice_list)
			# move up
			if move_direction[0] == 0:
				# remove walls
				Canvas_param.maze_tensor[cord[0], cord[1], 0] = 0
				cord = (cord[0] - 1, cord[1])
				Canvas_param.maze_tensor[cord[0], cord[1], 2] = 0

				# set tile to explored
				Canvas_param.maze_tensor[cord[0], cord[1], 4] = 0

				maze_stack.append(cord)

			# move right
			if move_direction[0] == 1:
				# remove walls
				Canvas_param.maze_tensor[cord[0], cord[1], 1] = 0
				cord = (cord[0], cord[1] + 1)
				Canvas_param.maze_tensor[cord[0], cord[1], 3] = 0

				# set tile to explored
				Canvas_param.maze_tensor[cord[0], cord[1], 4] = 0

				maze_stack.append(cord)

			# move down
			if move_direction[0] == 2:
				# remove walls
				Canvas_param.maze_tensor[cord[0], cord[1], 2] = 0
				cord = (cord[0] + 1, cord[1])
				Canvas_param.maze_tensor[cord[0], cord[1], 0] = 0

				# set tile to explored
				Canvas_param.maze_tensor[cord[0], cord[1], 4] = 0

				maze_stack.append(cord)

			# move left
			if move_direction[0] == 3:
				# remove walls
				Canvas_param.maze_tensor[cord[0], cord[1], 3] = 0
				cord = (cord[0], cord[1] - 1)
				Canvas_param.maze_tensor[cord[0], cord[1], 1] = 0

				# set tile to explored
				Canvas_param.maze_tensor[cord[0], cord[1], 4] = 0

				maze_stack.append(cord)

		# draw maze
		if Canvas_param.display_process:
			display_tensor(root, maze_canvas, Canvas_param, maze_stack)

	# dislay final product
	display_tensor(root, maze_canvas, Canvas_param, maze_stack)

	#give back control to user
	Canvas_param.displaying_maze = False

	return Canvas_param.maze_tensor
