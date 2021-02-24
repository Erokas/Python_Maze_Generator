import time


def possible_choices(maze_tensor, cord, algo_type):
	choice_list = []

	if algo_type == "deep":
		for i in range(4):
			if maze_tensor[cord[0], cord[1], i] == 1:
				if i == 0 and maze_tensor[cord[0] - 1, cord[1], 4] == 1:
					choice_list.append(i)
				elif i == 1 and maze_tensor[cord[0], cord[1] + 1, 4] == 1:
					choice_list.append(i)
				elif i == 2 and maze_tensor[cord[0] + 1, cord[1], 4] == 1:
					choice_list.append(i)
				elif i == 3 and maze_tensor[cord[0], cord[1] - 1, 4] == 1:
					choice_list.append(i)
	elif algo_type == "kruskal":
		# tile is set to zero if there are no possible choices
		if maze_tensor[cord[0], cord[1], 5] != 0:
			set_number = maze_tensor[cord[0], cord[1], 4]
			for i in range(4):
				if maze_tensor[cord[0], cord[1], i] == 1:
					if i == 0 and maze_tensor[cord[0] - 1, cord[1], 4] != set_number:
						choice_list.append(i)
					elif i == 1 and maze_tensor[cord[0], cord[1] + 1, 4] != set_number:
						choice_list.append(i)
					elif i == 2 and maze_tensor[cord[0] + 1, cord[1], 4] != set_number:
						choice_list.append(i)
					elif i == 3 and maze_tensor[cord[0], cord[1] - 1, 4] != set_number:
						choice_list.append(i)
	return choice_list


def draw_center_rectange(maze_canvas, x, y, square_border, color, rectange_width):
	square_distance_from_walls = (square_border / 2) - rectange_width

	# center the square in the tile
	maze_canvas.create_rectangle(x * square_border + square_distance_from_walls, y * square_border + square_distance_from_walls, (x * square_border +
																																  square_distance_from_walls) + 2 * rectange_width, (y * square_border + square_distance_from_walls) + 2 * rectange_width, fill=color)


def display_tensor(root, maze_canvas, Canvas_param, maze_stack=[]):
	# reset canvas
	maze_canvas.delete("all")

	# tensor line dimensions [top, right, bottom, right, exploration_indicator]
	for y in range(Canvas_param.shape[0]):
		for x in range(Canvas_param.shape[1]):

			# draw horizontal lines
			if Canvas_param.maze_tensor[y, x, 0] == 1:
				maze_canvas.create_line(Canvas_param.square_border * x, Canvas_param.square_border * y,
										Canvas_param.square_border * (x + 1), Canvas_param.square_border * y, fill=Canvas_param.line_color)

			# draw vertical lines
			if Canvas_param.maze_tensor[y, x, 1] == 1:
				maze_canvas.create_line(Canvas_param.square_border * (x + 1), Canvas_param.square_border * y,
										Canvas_param.square_border * (x + 1), Canvas_param.square_border * (y + 1), fill=Canvas_param.line_color)

			# draw maze creation path
			# make it not redraw start and end coordinates
			if (y, x) in maze_stack and (x, y) != (9, 7):
				draw_center_rectange(
					maze_canvas, x, y, Canvas_param.square_border, "yellow", Canvas_param.path_marker_width)

	# draw maze start indicator
	# change to get coordinates from variables
	# MAKE RECTANGE WIDTH CHANGE WITH CHOSEN MAZE DIMENSIONS
	draw_center_rectange(maze_canvas, Canvas_param.start_cord[1], Canvas_param.start_cord[0],
						 Canvas_param.square_border, "green", Canvas_param.path_marker_width)

	# draw maze end indicator
	draw_center_rectange(maze_canvas, Canvas_param.end_cord[1], Canvas_param.end_cord[0],
						 Canvas_param.square_border, "red", Canvas_param.path_marker_width)

	# draw borders
	border_thickness = 10
	border_color = "grey"

	# horizontal
	maze_canvas. create_line(
		0, 0, Canvas_param.canvas_width, 0, width=border_thickness, fill=border_color)
	maze_canvas. create_line(0, Canvas_param.canvas_height, Canvas_param.canvas_width,
							 Canvas_param.canvas_height, width=border_thickness, fill=border_color)

	# vertical
	maze_canvas. create_line(
		0, 0, 0, Canvas_param.canvas_height, width=border_thickness, fill=border_color)
	maze_canvas. create_line(Canvas_param.canvas_width, 0, Canvas_param.canvas_width,
							 Canvas_param.canvas_height, width=border_thickness, fill=border_color)

	root.update()

	# delay animation
	time.sleep(Canvas_param.standard_sleep_time / Canvas_param.speed_factor)
