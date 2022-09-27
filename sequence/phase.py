import logging

# Get logger object
logger = logging.getLogger(__name__)

class PhaseError(Exception):
        pass
        
class Phase(object):
        def __init__(self, name, color, action0):
                self.name = name
                self.color = color
                self.action0 = action0
                self.action1 = None
