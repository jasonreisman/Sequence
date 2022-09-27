#!/usr/bin/env python3

import argparse
import os.path
import sys
import logging
from sequence import sequence

# Default logging configuration
logging.basicConfig(level=logging.INFO)

# Get logger object
logger = logging.getLogger(__name__)

class MakeSequence(sequence.Sequence):
        def __init__(self, filename, loglevel=logging.INFO):
                self.sequence_lines = []
                # read actions into list
                self.parse_input_file(filename)
                # create drawing
                super().__init__(self.sequence_lines, loglevel=loglevel)


        def parse_input_file(self, filename):
                # read actions into file
                open_phases = []
                num_lines_processed = 0
                with open(filename, 'rt') as f:
                        for i, line in enumerate(f):
                                line = line.strip()
                                self.sequence_lines.append(line)

def main():
        logging_level = logging.INFO
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
        cmd_param.add_argument('--debug', '-d', dest='debug', default=False,
                               required=False, action='store_true',
                               help='Enable debug mode.')

        param = cmd_param.parse_args()
        if param.debug:
                logging_level = logging.DEBUG
                # change logger verbose level
                logger.setLevel(logging.DEBUG)
        txtin_flow_filename = param.inputfile
        svgout_flow_filename = param.outputfile

        logger.info('Process start')

        if not os.path.isfile(txtin_flow_filename):
                print(f'File {txtin_flow_filename} not found')
                sys.exit(-1)

        logger.info('Processing sequence text file')
        seq = MakeSequence(txtin_flow_filename, loglevel=logging_level)
        seq.build()

        logger.debug('SVG file: %s' %seq.to_string())

        with open(svgout_flow_filename, 'w') as f:
                print(seq.to_string(), file=f)
                logger.info('SVG file saved')

if __name__ == '__main__':
        main()
