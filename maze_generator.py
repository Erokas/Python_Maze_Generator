import numpy as np
from tkinter import *
from tkinter import ttk
import random
import time
from common_functions import possible_choices, display_tensor
from deep_search import solve_maze_deep_search
from kruskal import solve_maze_kruskal

def generate_maze_tensor(height, width):

	maze_tensor = np.ones((height, width, 6), dtype=int)

	# generate impassable barrier around the edges
	# top
	maze_tensor[0, :, 0] = 2

	# right
	maze_tensor[:, width - 1, 1] = 2

	# bottom
	maze_tensor[height - 1, :, 2] = 2

	# left
	maze_tensor[:, 0, 3] = 2

	return maze_tensor

def update_maze_dimensions(Canvas_param, UI_param):
	dimensions = UI_param.maze_dimensions_combobox.get()
	if dimensions == "10x8":
		Canvas_param.shape = (8, 10)
		Canvas_param.square_border = 100
		Canvas_param.path_marker_width = 10
	if dimensions == "20x16":
		Canvas_param.shape = (16, 20)
		Canvas_param.square_border = 50
		Canvas_param.path_marker_width = 5
	if dimensions == "40x32":
		Canvas_param.shape = (32, 40)
		Canvas_param.square_border = 25
		Canvas_param.path_marker_width = 3

def show_blank_maze(root, maze_canvas, Canvas_param, UI_param):
	#update dimensions
	update_maze_dimensions(Canvas_param, UI_param)

	#generate black maze map
	maze_tensor = generate_maze_tensor(*Canvas_param.shape)
	Canvas_param.maze_tensor = maze_tensor

	#display maze
	display_tensor(root, maze_canvas, Canvas_param)


def generate_maze(root, maze_canvas, Canvas_param, UI_param):
	#reset abort generation button
	Canvas_param.abort_generation = False

	# update program settings
	Canvas_param.display_process = UI_param.display_process_var.get()
	Canvas_param.speed_factor = UI_param.spinbox_var.get()
	Canvas_param.maze_type = UI_param.maze_type_combobox.get()

	# update maze dimensions
	update_maze_dimensions(Canvas_param, UI_param)

	maze_tensor = generate_maze_tensor(*Canvas_param.shape)
	Canvas_param.maze_tensor = maze_tensor

	if Canvas_param.maze_type == "deep_search":
		maze_tensor = solve_maze_deep_search(
			root, maze_tensor, Canvas_param.start_cord, Canvas_param.end_cord, maze_canvas, Canvas_param)
	elif Canvas_param.maze_type == "kruskal":
		maze_tensor = solve_maze_kruskal(
			root, maze_tensor, maze_canvas, Canvas_param)


# window parameters
class Canvas_parameters:
	def __init__(self):
		self.maze_tensor = None

		self.canvas_width = 1000
		self.canvas_height = 800
		self.bg_color = "black"
		self.line_color = "white"
		self.shape = (8, 10)
		self.square_border = 100
		self.display_process = False
		self.start_cord = (0, 0)
		self.end_cord = (7, 9)
		self.standard_sleep_time = 0.02
		self.speed_factor = 1
		self.path_marker_width = 10
		self.maze_type = "kruskal"
		self.displaying_maze = False

		self.mouse_cord = (0, 0)
		self.abort_generation = False

	def mouse_click(self, UI_param, event, root, maze_canvas):
		if not self.displaying_maze:
			#convert cord to tensor cord
			if UI_param.mouse_mode == "start":
				self.start_cord = (event.y // self.square_border, event.x // self.square_border)
			else:
				self.end_cord = (event.y // self.square_border, event.x // self.square_border)

			#redraw maze
			display_tensor(root, maze_canvas, self)

	def set_abort_generation(self):
		self.abort_generation = True




class UI_parameters:
	def __init__(self):
		self.maze_dimensions_options = ["10x8", "20x16", "40x32"]
		self.maze_type_options = ["deep_search", "kruskal"]
		self.lowest_speed_factor = 0.1
		self.highest_speed_factor = 20

		#what part of the maze is changed on click
		self.mouse_mode = "start"

	def create_UI_var(self, root):
		self.display_process_var = BooleanVar()
		self.spinbox_var = DoubleVar(root)
		self.spinbox_var.set(1.0)

	def switch_button_state(self, button_number):
		if button_number == 1:
			#switch pressed button off
			self.mouse_start_mode_button["bg"] = "light green"

			#turn the other button on
			self.mouse_end_mode_button["bg"] = "red"

			#change mouse click type
			self.mouse_mode = "start"
		else:
			#switch pressed button off
			self.mouse_end_mode_button["bg"] = "pink"

			#turn the other button on
			self.mouse_start_mode_button["bg"] = "green"

			#change mouse click type
			self.mouse_mode = "end"
			

	def create_widgets(self, root):
		self.maze_button = Button(root, text="Generate", pady=25, command=lambda: generate_maze(
			root, maze_canvas, Canvas_param, UI_param))
		self.abort_button = Button(root, text="Abort", pady=25, padx=20, command=Canvas_param.set_abort_generation)

		self.display_process_checkbutton = Checkbutton(
			root, text="Display Creation Process", variable=UI_param.display_process_var, onvalue=True, offvalue=False)
		self.speed_spinbox = Spinbox(root, from_=UI_param.lowest_speed_factor,
									 to=UI_param.highest_speed_factor, increment=0.1, textvariable=UI_param.spinbox_var)

		self.maze_dimensions_combobox = ttk.Combobox(
			root, value=UI_param.maze_dimensions_options)
		self.maze_dimensions_combobox.current(0)
		self.maze_dimensions_combobox.bind("<<ComboboxSelected>>", lambda x:show_blank_maze(root, maze_canvas, Canvas_param, UI_param))

		self.maze_type_combobox = ttk.Combobox(root, value=self.maze_type_options)
		self.maze_type_combobox.current(0)
		self.maze_type_combobox.bind("<<ComboboxSelected>>")

		self.mouse_start_mode_button = Button(root, bg="light green", padx=10, command=lambda: self.switch_button_state(1))
		self.mouse_end_mode_button = Button(root, bg="red", padx=10, command=lambda: self.switch_button_state(2))



# create classes
Canvas_param = Canvas_parameters()
UI_param = UI_parameters()

# declare window
root = Tk()
root.geometry("1000x900")

# STORE IN A CLASS
maze_canvas = Canvas(root, width=Canvas_param.canvas_width,
					 height=Canvas_param.canvas_height, bg=Canvas_param.bg_color)
maze_canvas.grid(row=2, column=0, columnspan=5)

maze_canvas.bind("<Button-1>", lambda x: Canvas_param.mouse_click(UI_param, x, root, maze_canvas))

# create UI
# create UI parameters class

UI_param.create_UI_var(root)
UI_param.create_widgets(root)


UI_param.maze_button.grid(row=0, column=0)
UI_param.abort_button.grid(row=0, column=1)
UI_param.display_process_checkbutton.grid(row=0, column=2)
UI_param.speed_spinbox.grid(row=1, column=2)
UI_param.maze_dimensions_combobox.grid(row=0, column=3)
UI_param.maze_type_combobox.grid(row=1, column=3)
UI_param.mouse_start_mode_button.grid(row=0, column=4)
UI_param.mouse_end_mode_button.grid(row=1, column=4)

# generate starting maze
show_blank_maze(root, maze_canvas, Canvas_param, UI_param)

root.mainloop()
