# Sequence
A tool for creating SVG sequence diagrams from text input files.

###Example
Sequence lets you make sequence diagrams that look like this:

<img src="http://jasonreisman.github.io/sequence/test.png" width="480">

from text input which looks like this:
```
# user tells server
@phase Request, #CD3F85
User, Browser, Clicks on link
Browser, Server, Opens socket using link address
Server, Browser, Accepts connection
Browser, Server, Requests page content
@endphase
@phase Synthesis, #C0C0FF
Server, Database, Requests page data
Database, Server, Returns page data
Server, Server, Generates page content
@endphase
@phase Response, #CD853F
# server responds
Server, Browser, Returns page content
Browser, Browser, Rasterizes content
Browser, User, Presents content
@endphase
```

### Prerequisites
You must have a python 2.7 installation and install the Python package `svgwrite`.

###Usage
```
./make_sequence.py <in filename> > <out filename>
```
