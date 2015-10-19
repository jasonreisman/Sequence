#!/usr/local/bin/python

import svgwrite

import os.path
import sys

class Colors:
	black = '#000000'
	gray = '#C0C0C0'

class Sequence:
	def __init__(self, filename):
		self.actors = []
		self.actors_map = {}
		self.actions = []
		# read actions into file
		with open(filename) as f:
			for i, line in enumerate(f):
				tokens = line.split(',')
				assert len(tokens) >= 3, 'line %i has less than 3 tokens' % (i)
				if len(tokens) < 3:
					continue
				actor0 = tokens[0].strip()
				actor1 = tokens[1].strip()
				action = tokens[2].strip()
				if actor0 not in self.actors_map:
					key = len(self.actors)
					self.actors_map[actor0] = key
					self.actors.append(actor0)
				if actor1 not in self.actors_map:
					key = len(self.actors)
					self.actors_map[actor1] = key
					self.actors.append(actor1)
				key0 = self.actors_map[actor0]
				key1 = self.actors_map[actor1]
				self.actions.append((key0, key1, action))
		# create drawing
		self.step_size = (100, 50)
		self.text_fudge = (0, 5)
		self.width = (len(self.actors) + 1)*self.step_size[0]
		self.height = (len(self.actions) + 2)*self.step_size[1]
		self.drawing = svgwrite.Drawing('out.svg', size=(self.width, self.height))

	def build(self):
		self.create_actors()
		self.create_actions()
		pass

	def to_string(self):
		return self.drawing.tostring()

	def create_actors(self):
		x = self.step_size[0]
		y = self.step_size[1]
		for name in self.actors:
			self.drawing.add(self.drawing.text(name, insert=(x, y - self.text_fudge[1]), stroke='none', fill=Colors.black, font_family="Helevetica", font_size="8pt", text_anchor="middle"))
			line = self.drawing.add(self.drawing.line((x, y), (x, self.height), stroke=Colors.gray, stroke_width=1))
			line.dasharray([5, 5])
			x += self.step_size[0]

	def create_actions(self):
		# create a marker objects
		start_marker = self.drawing.marker(insert=(3,3), size=(10,10), orient='auto')
		start_marker.add(self.drawing.circle((3, 3), r=3, fill=Colors.black))
		self.drawing.defs.add(start_marker)
		end_marker = self.drawing.marker(insert=(6,3), size=(10,10), orient='auto')
		end_marker.add(self.drawing.path("M0,0 L0,7 L6,3 L0,0", fill=Colors.black))
		self.drawing.defs.add(end_marker)
		# add actions
		y = 2*self.step_size[1]
		for (a0, a1, act) in self.actions:
			x0 = (a0 + 1)*self.step_size[0]
			x1 = (a1 + 1)*self.step_size[0]
			line = self.drawing.add(self.drawing.line((x0, y), (x1, y), stroke=Colors.black, stroke_width=1))
			line['marker-start'] = start_marker.get_funciri()
			line['marker-end'] = end_marker.get_funciri()
			self.drawing.add(self.drawing.text(act, insert=(0.5*(x0 + x1), y - self.text_fudge[1]), stroke='none', fill=Colors.black, font_family="Helevetica", font_size="6pt", text_anchor="middle"))
			y += self.step_size[1]

def usage():
	print 'Usage: ./make_sequence.py <in filename> > <out filename>'
	sys.exit(-1)

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print 'missing input filename'
		usage()
	filename = sys.argv[1]
	if not os.path.isfile(filename):
		print 'file %s not found' % filename
		sys.exit(-1)
	seq = Sequence(sys.argv[1])
	seq.build()
	print seq.to_string()