# Sequence
A tool for creating SVG sequence diagrams from text input files.

### Example
Sequence lets you make sequence diagrams that look like this:

<img src="http://jasonreisman.github.io/sequence/test.png" width="640`">

from text input which looks like this:
```
@phase Request, #CD3F85
# user clicks link
User, Browser, Clicks on link
# browser connects to server
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
# browser rasterizes and presents new page to user
Browser, Browser, Rasterizes content
Browser, User, Presents content
@endphase
```
###Data format

Sequence generates its SVG from a simple text data file.  There are two basic entities in the data file: _steps_ and _phases_.  Lines that begin with a hashtag (#) will be interpretted as comments, and have no effect on the image rendered.  Empty lines are also ignored.

####Steps

Each _step_ in the sequence, where a step is defined as _an action between two actors_, is a single line in the input data file.  (A step will be rendered as an arrow with text between actor columns.)  The line must be comma-separated and contain either three or four values.  The first value is the source actor, the one invoking the action.  The second entry is the target actor, the one receiving the action.  The third entry is a description of the action itself.  The fourth value is optional, but if present will be used as the step's color.

For example:
```
#Source Actor, Target Actor, Action Description
Client, Server, Makes Request
```

Or, if you'd like the arrow and text for the step to appear as green in the SVG:

```
#Source Actor, Target Actor, Action Description, Color
Client, Server, Makes Request, green
```

**Note #1**: there is no need (or way) to define actors explicity.  They are implicitly defined in the steps themselves.  Sequence will make sure that there is a single instance of each actor, even though the same actor may be reused in multiple steps

**Note #2**: if the source actor and target actor are the same, then no arrow will be drawn between the actors.  Instead a dot will appear in the source/target actor column with the text describing the action.

####Phases

A _phase_ is a collection of steps which will visually grouped together in the SVG.  Phases are opened by the special directive in the data `@phase`.  When opening a phase you will need to supply the name for the phase.  This is just text included after the open phase directive.  For example:

```
@phase Encryption
```

Like steps, you can also optionally define a color for the phase.  For example, to make the encryption phase red:

```
@phase Encryption, red
```

Phases are closed using another special directive, `@endphase`.  The end phase directive doesn't take any arguments.  Any extra text on the line will be ignored.  A full example showing opening and closing a phase is:

```
Bob, Keystore, Publishes public key
Bob, Alice, Requests senstive material
Alice, Alice, Writes sensitive message
@phase Encryption
Alice, Keystore, Retrieves Bob's public key
Alice, Alice, Encrypts message w/ pub key
@endphase
Alice, Bob, Sends encrypted message
Bob, Bob, Decrypts message w/ priv key
```

which produces this SVG:

<img src="http://jasonreisman.github.io/sequence/alice_bob.png" width="480`">

####Ordering

By defaults, actors will be rendered from left to right in the order that they appear in the sequence file.  However, if you want to specify a specific order for the actors in your diagram, you can do so by using the `@order` directive as the first line in your sequence file, followed by the (comma separated) specific actor order that you'd like to see.  Comment and blank lines may preceed `@order`, but nothing else.

For instance, if we wanted to change the previous example to be in the order Alice, Bob, Keystore (instead of Bob, Keystore, Alice) we could add a `@order` directive at the top:

```
@order Alice, Bob, Keystore
Bob, Keystore, Publishes public key
Bob, Alice, Requests senstive material
Alice, Alice, Writes sensitive message
@phase Encryption
Alice, Keystore, Retrieves Bob's public key
Alice, Alice, Encrypts message w/ pub key
@endphase
Alice, Bob, Sends encrypted message
Bob, Bob, Decrypts message w/ priv key
```

which then produces this SVG:

<img src="http://jasonreisman.github.io/sequence/alice_bob_ordered.png" width="480`">

Any actors not specified in the `@order` directive will appear in the order they appear in the rest of the file.

### Prerequisites
You must have a python 2.7 installation and install the Python package `svgwrite` (e.g., `pip install svgwrite`)

###Usage
```
python make_sequence.py in.seq > out.svg
```
