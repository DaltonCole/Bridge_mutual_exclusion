# Programmer: Dalton Cole, Josh Herman, Neil Blood
# Class: CS5800, Distributed Operating Systems
# Assignment: Programming Project 1

from tkinter import *
from random import choice, randint
from time import time

# Person class
# Represents a person on a bridge
class Person:

	"""Initializes the person Class

		:param int person: The integer that corresponds to a shape on the canvas
		:param string walking_speed: The speed a person walks at (Slow, Medium, Fast, or Super Fast)

		:return: None
	"""
	def __init__(self, person, walking_speed):
		# Shape object
		self.person = person
		# Set walking speed
		self.set_speed(walking_speed)
		# Default wanting to be on the left side
		self.side = 0 # 0 if on or going to left side, 1 if on or going to right side
		# Time stamp of when a person wants to cross the bridge
		self.time_stamp = None

	"""Sets the walking speed for a person

		:param string walking_speed: The speed a person walks at (Slow, Medium, Fast, or Super Fast)

		:return: None
	"""
	def set_speed(self, walking_speed):
		if walking_speed == 'Slow':
			self.walking_speed = randint(1,10) / 50
		elif walking_speed == 'Medium':
			self.walking_speed = randint(25,50) / 50
		elif walking_speed == 'Fast':
			self.walking_speed = randint(100, 200) / 50
		elif walking_speed == 'Super Fast':
			self.walking_speed = randint(500, 1000) / 50
		elif walking_speed == 'Blazing':
			self.walking_speed = randint(1000, 5000) / 50

	"""Sets the side the person is going towards

		:param int side: 0 if wanting to be on the left side, 1 if wanting to be on the right side

		:return: None
	"""
	def set_side(self, side):
		self.side = side


class Bridge:
	"""Initializes the bridge Class
		Sets default speed to 'Super Fast'
		Sets default algorithm to 'Ricart & Agrawalas'
		Sets default person count to 10
		Sets c_size (person size) to 10
		Initializes the set of points a user can spawn on

		:param tkinter root: The integer that corresponds to a shape on the canvas

		:return: None
	"""
	def __init__(self, root):
		# GUI 
		self.root = root
		# Current speed
		self.speed = 'Super Fast'
		# Current algorithm
		self.algorithm = 'Ricart & Agrawalas'
		# Current person count
		self.count = 10
		# Current people
		self.people = []
		# Person size
		self.c_size = 10 #c ircle size
		# Spawn-able points (left and right corners)
		self.points = ((100, 450), (100, 50), (900, 50), (900, 450))

		# Create the canvas
		self.make_canvas()
		# Create the menu drop-downs and buttons
		self.make_menues()
		# Create the path
		self.make_bridge()
		# Create people
		self.make_people()
		# Move people
		self.move_people()

	"""Creates a canvas for the bridges to appear on
		Sets application title to "Bridge"
		Makes application un-resizable
		Creates a 1000 x 500 canvas

		:return: None
	"""
	def make_canvas(self):
		# Set application title
		self.root.title("Bridge")
		# Make window not re-sizable
		self.root.resizable(False, False)
		# Create canvas
		self.canvas = Canvas(self.root, width = 1000, height = 500, background='white')

	"""Makes menus for the canvas
		Creates the Walking Speed, algorithm, and number of people drop down menus and buttons

		:return: None
	"""
	def make_menues(self):
		''' Menu is in the following form:
			
			Walking Speed | Algorithm  | Person total
			------------------------------------------
			Speed button  | Alg button | Person button
			------------------------------------------
			        BRIDGE (Added in make_bridge)

		'''

		### Walking Speed ###
		# Make drop Down menu
		default_walking_speed = StringVar(self.root)
		default_walking_speed.set(self.speed)
		walking_speed = OptionMenu(self.root, default_walking_speed, 'Slow', 'Medium', 'Fast', 'Super Fast', 'Blazing')
		walking_speed.grid(row=0, column=0)
		# Make button to confirm drop down menu
		set_walking_speed = lambda: self.set_walking_speed(default_walking_speed.get())
		speed_button = Button(self.root, text='Set Walking Speed', command=set_walking_speed)
		speed_button.grid(row=1, column=0)

		### Make Algorithm Choice ###
		# Make drop down Menu
		default_algorithm = StringVar(self.root)
		default_algorithm.set(self.algorithm)
		algorithm = OptionMenu(self.root, default_algorithm, 'Ricart & Agrawalas', 'Personal')
		algorithm.grid(row=0, column=1)
		# Make button to confirm drop down menu
		set_algorithm = lambda: self.set_algorithm(default_algorithm.get())
		algorithm_button = Button(self.root, text='Set Algorithm', command=set_algorithm)
		algorithm_button.grid(row=1, column=1)

		### Make number of nodes Choice ###
		# Make text field
		default_count = StringVar(self.root)
		default_count.set(self.count)
		count = Entry(self.root, textvariable=default_count)
		count.grid(row=0, column=2)
		# Make button to confirm text field
		set_count = lambda: self.set_count(default_count.get())
		count_button = Button(self.root, text='Set Person Count', command=set_count)
		count_button.grid(row=1, column=2)

	"""Creates the path shapes (two triangles and a line)

		:return: None
	"""
	def make_bridge(self):
		'''
		(100, 50)	|\                  /| (900, 50)
			        | \                / |
			        |  \              /  |
			        |   \            /   |
			        |    \(350,250) /    |
			        |     ----------     |
			        |    / (650,250)\    |
			        |   /            \   |
			        |  /              \  |
			        | /                \ |
		(100, 450)  |/                  \| (900, 450)
		'''

		self.canvas.grid(row=2,column=0,columnspan=3)
		# Left triangle
		self.canvas.create_polygon((100, 450, 350, 250, 100, 50), fill='white', outline='black')
		# Right triangle
		self.canvas.create_polygon((900, 450, 650, 250, 900, 50), fill='white', outline='black')
		# Line between triangles
		self.canvas.create_line((350,250, 650,250))

	"""Makes self.count number of people with random rrggbb colors and adds the person to 
		self.people list

		:return: None
	"""
	def make_people(self):
		for i in range(self.count):
			sp = choice(self.points) # Starting point
			shape = self.canvas.create_oval((sp[0] - self.c_size, sp[1] + self.c_size, sp[0] + self.c_size, sp[1] - self.c_size), fill=self.random_color())
			self.people.append(Person(shape, self.speed))

	"""Moves people based on their current position on the grid and according to the bridge protocol

		:return: None
	"""
	def move_people(self):
		try:
			for i in self.people:
				# Coordinates of person
				coords = self.canvas.coords(i.person)

				# Paths are numbered such that the path going up on the
				# left triangle is 1, then 2, and finally 8 going from the west
				# side of the bridge to the bottom left corner

				### 1-2 ###
				# On top of right triangle, go South East
				if(coords[0] == 100 - self.c_size and coords[1] == 50 - self.c_size):
					self.canvas.move(i.person, 1 * i.walking_speed, .8 * i.walking_speed)

				### 2-3 ###
				# Cross bridge going east
				elif(coords[0] == 350 - self.c_size and coords[1] == 250 - self.c_size and i.side == 1):
					self.cross_bridge(i)

				### 3-4 ###
				# Just crossed bridge going east, go North East
				elif(coords[0] == 650 - self.c_size and coords[1] == 250 - self.c_size and i.side == 1):
					self.canvas.move(i.person, (1 * i.walking_speed), (-.8 * i.walking_speed))
					i.time_stamp = None # Reset Time stamp

				### 4-5 ###
				# Move down on straight triangle
				elif(coords[0] == 900 - self.c_size and coords[1] == 50 - self.c_size):
					self.canvas.move(i.person, 0, i.walking_speed)

				### 5-6 ###
				# On bottom of left triangle, go North West
				elif(coords[0] == 900 - self.c_size and coords[1] == 450 - self.c_size):
					self.canvas.move(i.person, -(1 * i.walking_speed), (-.8 * i.walking_speed))

				### 6-7 ###
				# Cross bridge going west
				elif(coords[0] == 650 - self.c_size and coords[1] == 250 - self.c_size and i.side == 0):
					self.cross_bridge(i)

				### 7-8 ###
				# Just crossed bridge going west, go South West
				elif(coords[0] == 350 - self.c_size and coords[1] == 250 - self.c_size and i.side == 0):
					self.canvas.move(i.person, (-1 * i.walking_speed), (.8 * i.walking_speed))
					i.time_stamp = None # Reset Time stamp

				### 8-1 ###
				# Move up straight away triangle
				elif(coords[0] == 100 - self.c_size and coords[1] == 450):
					self.canvas.move(i.person, 0, -i.walking_speed)

				### 1 ###
				# Move up on straight away triangle
				elif(coords[0] == 100 - self.c_size and coords[1] < 450):
					# Go full distance if far away from (100, 50)
					if(coords[1] - i.walking_speed >= 50 - self.c_size):
						self.canvas.move(i.person, 0, - i.walking_speed)
					# Go parital distance if close to (100, 50)
					else:
						self.canvas.move(i.person, 0, - (coords[1] - (50 - self.c_size)))

				### 2 ###
				# Head towards left side of bridge
				elif(coords[0] > 100 - self.c_size and coords[0] < 350 - self.c_size and coords[1] < 250 - self.c_size):
					# Go full distance if far away from (350,250):
					if(coords[1] + i.walking_speed <= 250 - self.c_size):
						self.canvas.move(i.person, 1 * i.walking_speed, .8 * i.walking_speed)
					else:
						self.canvas.move(i.person, ((350 - self.c_size) - coords[0]), ((250 - self.c_size) - coords[1]))
						i.set_side(1)
				
				### 3 ###
				### 7 ###
				# Move across bride
				elif(coords[0] > 350 - self.c_size and coords[0] < 650 - self.c_size and coords[1] == 250 - self.c_size):
					### 3 ###
					# Going East
					if(i.side == 1):
						# Go full distance if far away from (650, 250)
						if(coords[0] + i.walking_speed <= 650 - self.c_size):
							self.canvas.move(i.person, i.walking_speed, 0)
						# Go partial distance if close to (650, 250)
						else:
							self.canvas.move(i.person, (650 - self.c_size - coords[0]), 0)
					### 7 ###
					# Going West
					else:
						# Go full distance if far away from (350, 250)
						if(coords[0] - i.walking_speed >= 350 - self.c_size):
							self.canvas.move(i.person, -i.walking_speed, 0)
						# Go partial distance if close to (350, 250)
						else:
							self.canvas.move(i.person, -(coords[0] - (350 - self.c_size)), 0)

				### 4 ###
				# Head towards top right corner
				elif(coords[0] > 650 - self.c_size and coords[0] < 900 - self.c_size and coords[1] < 250 - self.c_size):
					# Go full distance if far away from (900, 50):
					if(coords[1] - i.walking_speed >= 50 - self.c_size):
						self.canvas.move(i.person, (1 * i.walking_speed), (-.8 * i.walking_speed))
					# Go partial distance if close to (900, 50)
					else:
						self.canvas.move(i.person, (900 - self.c_size - coords[0]), -(coords[1] - (50 - self.c_size)))

				### 5 ###
				# Move down on straight away triangle
				elif(coords[0] == 900 - self.c_size and coords[1] > 50 - self.c_size):
					# Go full distance if far away from (900, 450)
					if(coords[1] + i.walking_speed <= 450 - self.c_size):
						self.canvas.move(i.person, 0, i.walking_speed)
					# Go partial distance if close to (900, 450)
					else:
						self.canvas.move(i.person, 0, ((450 - self.c_size) - coords[1]))

				### 6 ###
				# Head towards right side of bridge
				elif(coords[0] > 650 - self.c_size and coords[0] < 900 - self.c_size and coords[1] > 250 - self.c_size):
					# Go full distance if far away from (650, 250):
					if(coords[0] - i.walking_speed >= 650 - self.c_size):
						self.canvas.move(i.person, (-1 * i.walking_speed), (-.8 * i.walking_speed))
					# Go partial distance if close to (650, 250):
					else:
						self.canvas.move(i.person, -(coords[0] - (650 - self.c_size)), -(coords[1] - (250 - self.c_size)))
						i.set_side(0)

				### 8 ###
				# Head towards bottom left corner
				elif(coords[0] > 100 - self.c_size and coords[0] < 350 - self.c_size and coords[1] > 250 - self.c_size):
					# Go full distance if far away from (100, 450):
					if(coords[1] + i.walking_speed <= 450 - self.c_size):
						self.canvas.move(i.person, (-1 * i.walking_speed), (.8 * i.walking_speed))
					# Go partial distance if close to (100, 450):
					else:
						self.canvas.move(i.person, ((100 - self.c_size) - coords[0]), ((450 - self.c_size) - coords[1]))
				
		except Exception as e: print(e)

		# Call again after 10 ms
		self.root.after(10, self.move_people)

	"""Makes the person take the first step across the bridge is able to

		:param Person person: The person trying to cross the bridge

		:return: None
	"""
	def cross_bridge(self, person):
		if(self.algorithm == 'Ricart & Agrawalas'):
			# If we can cross the bridge, do so
			if(self.bridge_single_person(person)):
				# If wanting to go East, go East
				if(person.side == 1):
					self.canvas.move(person.person, person.walking_speed, 0)
				# Else West
				else:
					self.canvas.move(person.person, -person.walking_speed, 0)
		else:
			# If we can cross the bridge, do so
			if(self.bridge_multiple_people(person)):
				# If wanting to go East, go East
				if(person.side == 1):
					self.canvas.move(person.person, person.walking_speed, 0)
				# Else West
				else:
					self.canvas.move(person.person, -person.walking_speed, 0)

	"""Determines if the person can cross the bridge when only one person can be on the bridge at a time
		
		:param Person person: The person attempting to cross the bridge

		:return: If the person can cross the bridge or not

		:rType: Bool
	"""
	def bridge_single_person(self, person):
		# Set time stamp
		if person.time_stamp == None:
			person.time_stamp = time()

		# Number of people who have said it's okay to cross the bridge
		acked = 0

		# Check each process's time stamp
		for i in self.people:
			# If no time stamp, receive ack
			if i.time_stamp == None:
				acked += 1
			# If your time stamp is lower, you receive ack
			elif i.time_stamp > person.time_stamp:
				acked += 1

			# If someone is already on the bridge, return false
			# NOTE: This is only necessary when switching between protocols
			coords = self.canvas.coords(i.person)
			if(coords[0] > 350 - self.c_size and coords[0] < 650 - self.c_size):
				return False

		# If everyone else acked you, then you may cross the bridge
		if(acked == int(self.count) - 1):
			return True

		return False

	
	"""Determines if the person can cross the bridge when multiple people can be on the bridge at a time
		If you are moving in the same direction as the person with the lowest
		time stamp, then you may cross the bridge	
	

		:param Person person: The person attempting to cross the bridge

		:return: If the person can cross the bridge or not

		:rType: Bool
	"""
	def bridge_multiple_people(self, person):
		# Set time stamp
		if person.time_stamp == None:
			person.time_stamp = time()

		# lowest time stamp [time stamp, direction]
		lowest_time = [person.time_stamp, person.side]

		# Number of people currently on the bridge
		people_on_bridge = 0

		for i in self.people:
			coords = self.canvas.coords(i.person)
			if i.time_stamp != None:
				if i.time_stamp < lowest_time[0]:
					lowest_time[0] = i.time_stamp
					lowest_time[1] = i.side

			# Find the number of people going a direction on the bridge
			# >0 means going East
			# <0 means going West
			if(coords[0] > 350 - self.c_size and coords[0] < 650 - self.c_size):
				if i.side == 1:
					people_on_bridge += 1
				else:
					people_on_bridge -= 1

		# If we are not on the same side as the person with the lowest
		# time stamp, return false
		if(person.side != lowest_time[1]):
			return False

		# If no one is on the bridge, cross it
		if(people_on_bridge == 0):
			return True

		# If someone of your affinity is on the bridge and the person with the lowest time stamp
		# is on your side, cross the bridge
		if(people_on_bridge < 0 and person.side == 0):
			return True
		elif(people_on_bridge > 0 and person.side == 1):
			return True

		return False


	"""Sets the walking speed of a person. Called when walking speed button is pressed	
	
		:param string walking_speed: The speed of someone crossing the bridge

		:return: None
	"""
	def set_walking_speed(self, walking_speed):
		self.speed = walking_speed

		for i in self.people:
			i.set_speed(self.speed)

		print(self.speed)

	"""Sets the bridge algorithm. Called when algorithm button is pressed	
	
		:param string algorithm: The algorithm used to cross the bridge

		:return: None
	"""
	def set_algorithm(self, algorithm):
		self.algorithm = algorithm
		print(self.algorithm)

	"""Sets the number of people. Called when people count button is pressed	
	
		:param string count: The number of people on the canvas

		:return: None
	"""
	def set_count(self, count):
		self.count = count

		# Set max count to 100 (so there isn't lag)
		if int(self.count) > 100:
			self.count = 100

		# Add more people
		while(int(self.count) > len(self.people)):
			sp = choice(self.points) # start point
			shape = self.canvas.create_oval((sp[0] - self.c_size, sp[1] + self.c_size, sp[0] + self.c_size, sp[1] - self.c_size), fill=self.random_color())
			self.people.append(Person(shape, self.speed))
		
		# Remove people
		while(int(self.count) < len(self.people)):
			shape = choice(self.people)
			self.people.remove(shape)
			self.canvas.delete(shape.person)

		print(self.count)

	"""Creates a random rrggbb value
	
		:return: A random rrggbb value. Ex: '#c0ffee'
	"""
	def random_color(self):
		hex_colors = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
		return '#' + choice(hex_colors) + choice(hex_colors) + choice(hex_colors) + choice(hex_colors) + choice(hex_colors) + choice(hex_colors)

root = Tk()
ex = Bridge(root)

print("Entering GUI")
root.mainloop()