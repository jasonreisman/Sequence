# Sequence
A tool for creating SVG sequence diagrams from text input files.

###Example
Sequence lets you make sequence diagrams that look like this:

From text input which looks like this:
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

###Usage
'''./make_sequence.py <in filename> > <out filename>'''
