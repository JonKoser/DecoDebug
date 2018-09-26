This is a decorator package that I made so I could practice working with decorators.
DecoDebug will print out and log basic debug information such as:
- Values of all arguments being passed into a function
- The return value of a function
- The number of times that function has been called

It works by decorating each function in question with @Debug(<optional_level>) where <optional_level>
is the debugging priority level. This can be set so not all decorated functions output debug information
if a user only cares about some important ones.
The @DecoDebugMain decorator can be added to the script's main method so that debugging can be turned on
and off and the level set from the command line.
If @DecoDebugMain isn't used, users can also set an environment variable called "DECO_DEBUG_LEVEL" to 
start debugging.
Anyway, this was a projct I mainly did to occupy a small chunk of time on a 14 hour plane flight so there's still plenty
of work to be done yet. Maybe someone will find it helpful though :)
