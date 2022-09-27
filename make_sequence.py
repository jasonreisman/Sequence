#!/usr/bin/env python3

import svgwrite
import argparse
import os.path
import sys
import logging

logging.basicConfig(level=logging.DEBUG)

class Colors:
        black = '#000000'
        gray = '#C0C0C0'

class PhaseError(Exception):
        pass
        
class Phase(object):
        def __init__(self, name, color, action0):
                self.name = name
                self.color = color
                self.action0 = action0
                self.action1 = None

class Sequence(object):
        def __init__(self, filename):
                self.filename = filename
                self.actors = []
                self.actors_map = {}
                self.actions = []
                self.phases = []
                # read actions into file
                self.parse_input_file(filename)
                # create drawing
                self.top_left = (100, 50)
                self.step_size = (100, 25)
                self.text_fudge = (0, 5)
                self.width = self.top_left[0] + (len(self.actors) + 1)*self.step_size[0]
                self.height = self.top_left[1] + (len(self.actions) + 1)*self.step_size[1]
                self.drawing = svgwrite.Drawing(size=(self.width, self.height))
                self.markers = {}

        def parse_input_file(self, filename):
                # read actions into file
                open_phases = []
                num_lines_processed = 0
                with open(filename) as f:
                        for i, line in enumerate(f):
                                line = line.strip()
                                logging.debug('New line: %s' % line)
                                if len(line) == 0:
                                        logging.debug('skip empty lines')
                                        continue
                                if line[0] == '#':
                                        logging.debug('skip comments')
                                        continue
                                if line.startswith('@phase'):
                                        logging.debug('opens a phase')
                                        tokens = [s.strip() for s in line[len('@phase'):].split(',')]
                                        assert len(tokens) > 0, '@phase must contain at least a name'
                                        phase_name = tokens[0]
                                        assert len(phase_name) > 0, '@phase must contain at least a name'
                                        phase_color = tokens[1] if len(tokens) > 1 else Colors.gray
                                        p = Phase(phase_name, phase_color, len(self.actions))
                                        open_phases.append(p)
                                        logging.debug('total open phases: %d' % len(open_phases))
                                elif line.startswith('@endphase'):
                                        logging.debug('ends a phase')
                                        assert len(open_phases) > 0, '@endphase found with no corresponding opening @phase'
                                        p = open_phases.pop()
                                        p.action1 = len(self.actions)
                                        self.phases.append(p)
                                elif line.startswith('@order'):
                                        logging.debug('order line')
                                        assert num_lines_processed==0, '@order may only be on the first line!'
                                        tokens = [s.strip() for s in line[len('@order'):].split(',')]
                                        for t in tokens:
                                                key = len(self.actors)
                                                self.actors_map[t] = key
                                                self.actors.append(t)
                                else:
                                        logging.debug('process a flow line')
                                        self.parse_step(line)
                                num_lines_processed += 1
                if len(open_phases) != 0:
                        raise PhaseError('@phase opened without corresponding closing @endphase')

        def parse_step(self, line):
                tokens = [s.strip() for s in line.split(',')]
                assert len(tokens) >= 3, 'line %i has less than 3 tokens' % (i)
                if len(tokens) < 3:
                        return
                actor0 = tokens[0]
                actor1 = tokens[1]
                action = tokens[2]
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
                color = Colors.black
                if len(tokens) > 3:
                        color = tokens[3].strip()
                self.actions.append((key0, key1, action, color))


        def build(self):
                self.create_header()
                self.create_actors()
                self.create_phases()
                self.create_actions()
                pass

        def to_string(self):
                return self.drawing.tostring()

        def create_header(self):
                text = 'filename: %s' % self.filename
                self.drawing.add(self.drawing.text(text, insert=(self.top_left[0] - 0.5*self.step_size[0], 0.5*self.top_left[1]), stroke='none', fill=Colors.gray, font_family="Helevetica", font_size="8pt", text_anchor="start"))

        def create_phases(self):
                for phase in self.phases:
                        action0 = self.actions[phase.action0]
                        action1 = self.actions[phase.action1 - 1]

                        left = len(self.actors) + 1
                        right = -1
                        for action in self.actions[phase.action0:phase.action1]:
                                mn = min(action[0:2])
                                mx = max(action[0:2])
                                left = mn if mn < left else left
                                right = mx if mx > right else right
                        x = self.top_left[0] + (left - 0.5)*self.step_size[0]
                        y = self.top_left[1] + (phase.action0 + 0.5)*self.step_size[1]
                        w = (right - left + 1)*self.step_size[0]
                        h = (phase.action1 - phase.action0 - 0.125)*self.step_size[1]
                        filled_rect = self.drawing.add(self.drawing.rect((x,y), (w,h)))
                        filled_rect.fill(phase.color, None, 0.15)
                        self.drawing.add(self.drawing.rect((x,y), (w,h), stroke=phase.color, stroke_width=1, fill='none'))
                        transform = 'rotate(180,%i,%i) translate(6,0)' % (x, y+0.5*h)
                        self.drawing.add(self.drawing.text(phase.name, insert=(x, y+0.5*h), stroke='none', fill=phase.color, font_family="Helevetica", font_size="6pt", text_anchor="middle", writing_mode="tb", transform=transform))

        def create_actors(self):
                x = self.top_left[0]
                y = self.top_left[1]
                for name in self.actors:
                        self.drawing.add(self.drawing.text(name, insert=(x, y - self.text_fudge[1]), stroke='none', fill=Colors.black, font_family="Helevetica", font_size="8pt", text_anchor="middle"))
                        line = self.drawing.add(self.drawing.line((x, y), (x, self.height), stroke=Colors.gray, stroke_width=1))
                        line.dasharray([5, 5])
                        x += self.step_size[0]

        def create_actions(self):
                markers = {}
                # add actions
                y = self.top_left[1] + self.step_size[1]
                for (a0, a1, act, color) in self.actions:
                        x0 = self.top_left[0] + a0*self.step_size[0]
                        x1 = self.top_left[0] + a1*self.step_size[0]
                        if a0 == a1:
                                self.drawing.add(self.drawing.circle((x0, y), r=2, fill=color))
                        else:
                                start_marker, end_marker = self.get_markers(color)
                                assert start_marker is not None
                                assert end_marker is not None
                                line = self.drawing.add(self.drawing.line((x0, y), (x1, y), stroke=color, stroke_width=1))
                                line['marker-start'] = start_marker.get_funciri()
                                line['marker-end'] = end_marker.get_funciri()
                        self.drawing.add(self.drawing.text(act, insert=(0.5*(x0 + x1), y - self.text_fudge[1]), stroke='none', fill=color, font_family="Helevetica", font_size="6pt", text_anchor="middle"))
                        y += self.step_size[1]

        def get_markers(self, color):
                # create or get marker objects
                start_marker, end_marker = None, None
                if color in self.markers:
                        start_marker, end_marker = self.markers[color]
                else:
                        start_marker = self.drawing.marker(insert=(2,2), size=(10,10), orient='auto')
                        start_marker.add(self.drawing.circle((2,2), r=2, fill=color))
                        self.drawing.defs.add(start_marker)
                        end_marker = self.drawing.marker(insert=(6,3), size=(10,10), orient='auto')
                        end_marker.add(self.drawing.path("M0,0 L0,7 L6,3 L0,0", fill=color))
                        self.drawing.defs.add(end_marker)        
                        self.markers[color] = (start_marker, end_marker)
                return start_marker, end_marker


def main():
        # Parameters
        cmd_param = argparse.ArgumentParser(
                description='A tool for creating SVG sequence diagrams from text input files.')
        cmd_param.add_argument('--in', '-i', dest='inputfile',
                               metavar='text_flow_filename',
                               type=str, required=True,
                               help='Flow text file input.')
        cmd_param.add_argument('--out', '-o', dest='outputfile',
                               metavar='svg_filename', type=str,
                               required=True,
                               help='This is the result svg file.')

        param = cmd_param.parse_args()

        txtin_flow_filename = param.inputfile
        svgout_flow_filename = param.outputfile

        if not os.path.isfile(txtin_flow_filename):
                print(f'File {txtin_flow_filename} not found')
                sys.exit(-1)

        seq = Sequence(txtin_flow_filename)
        seq.build()
        print(seq.to_string())

        with open(svgout_flow_filename, 'w') as f:
                print(seq.to_string(), file=f)

 
if __name__ == '__main__':
        main()
