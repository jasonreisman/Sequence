# Sequence
A tool for creating SVG sequence diagrams from text input files.

###Example
Sequence lets you make sequence diagrams that look like this:

<img src="http://jasonreisman.github.io/sequence/test.png" width="480">

from text input which looks like this:
```
User, Browser, Clicks on link
Browser, Server, Opens socket using link address
Server, Browser, Accepts connection
Browser, Server, Requests page content
Server, Server, Loads content from storage, red
Server, Browser, Returns page content
Browser, Browser, Renders content
Browser, User, Displays content
```

### Prerequisites
You must have a python 2.7 installation and install the Python package `svgwrite`.

###Usage
```
./make_sequence.py <in filename> > <out filename>
```
