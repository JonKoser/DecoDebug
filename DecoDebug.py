#----------------------------------------------------------------------
# Name:    DecoDebug.py
# Purpose: A decorator library for adding debug functionality to a
#          Python program
# Author:  Jon Koser
#----------------------------------------------------------------------
from functools import wraps
import os
import sys

class Log():
    # TODO: Make the logger like the scriptLogger in general_util.py
    def __init__(self):
        self.logfile_dir = os.path.dirname(__file__)

    def message(self, message):
        filepath = os.path.join(self.logfile_dir, "Debug_Info.txt")
        print(message)
        with open(filepath, 'a+') as logfile:
            logfile.write(message + '\n')

log = Log()

class Debug():
    """
    Decorator for debugging purposes. Prints to log all the arguments given to a function, the number
    of times it has been called, and the output value.
    """
    def __init__(self, given_debug_level=0):
        """
        Sets up a function with the debugger
        :param given_debug_level: Optional: the level at which to print out. The lower the number, the more important. But, nothing
        can be lower than 0.
        """
        if given_debug_level < 0:
            given_debug_level = 0
        self.func_debug_level = given_debug_level
        self.call_count = 0

    def __call__(self, func):
        """
        This is what executes the wrapping of the function
        :param func: The function to wrap
        :return: The wrapped function
        """
        functionName = func.__name__
        @wraps(func)
        def wrapper(*args, **kwargs):
            """
            The wrapper that "becomes" the old function. Gets called every time the function is executed.
            :param args: All the arguments given to the function
            :param kwargs:  All the keword arguments given to the function
            :return: The results of the function - either wrapped or not depending on debug level
            """
            if (self.func_debug_level <= global_debug_level()):
                # TODO: Format everything better
                log.message("=== START DEBUG INFO FOR {} ===".format(functionName))
                if args or kwargs:
                    log.message("- VALUES OF ARGUMENTS IN FUNCTION {}:".format(functionName))
                    for arg in args:
                        log.message("--> {}".format(str(arg)))
                    for kword, value in kwargs.items():
                        log.message("--> {}: {}".format(str(kword), str(value)))
                self.call_count += 1
                log.message("- OUTPUT OF FUNCTION {}:".format(functionName))
                return_val = func(*args, **kwargs)
                if return_val:
                    log.message("- RETURN VALUE OF FUNCTION {}:".format(functionName))
                    log.message("--> {}".format(return_val))
                log.message("- {} HAS BEEN CALLED {} TIMES".format(functionName, self.call_count))
                log.message("=== END DEBUG INFO FOR {} ===".format(functionName))
                log.message('\n')
                return return_val
            else:
                return func(*args, **kwargs)
        return wrapper


class DecoDebugMain():
    """
    Decorator to be used on the main driving function of a program. This allows the command line to be parsed for
    DecoDebug parameters. Not needed to run the debugger though. The necessary environment variable can be set in other
    ways.
    """
    def __init__(self, func):
        """
        Initialization of the decorator.
        :param func: The main function
        """
        self.func = func
    def __call__(self, *args, **kwargs):
        """
        This is what executes the wrapping of the function
        :param args:
        :param args: Arguments provided to the main function
        :param kwargs: Keyword arguments provided to the main function
        :return: The wrapper executed
        """
        @wraps(self.func)
        def wrapper(*args, **kwargs):
            """
            This acts as the wrapper around the main function
            :param args: Arguments provided to the main function
            :param kwargs: Keyword arguments provided to the main function
            :return: The main function executed
            """
            #TODO: properly parse command line arguments
            if len(sys.argv) > 1:
                if sys.argv[1] == '--deco_debug':
                    try:
                        debugLevel = sys.argv[2]
                    except IndexError:
                        debugLevel = 9999
                    global GLOBAL_DEBUG_LEVEL
                    GLOBAL_DEBUG_LEVEL = int(debugLevel)
            return self.func(*args, **kwargs)
        return wrapper(*args, **kwargs)

def global_debug_level():
    """
    This function sets up the variable that determines which debug levels get to run
    :return: The level at which the test can run. Anything <= this number can run. This
    variable can either be set via command line using @DecoDebugMain over the main method
    or using an environment variable ("DECO_DEBUG_LEVEL").
    """
    global GLOBAL_DEBUG_LEVEL
    try:
        return GLOBAL_DEBUG_LEVEL
    except NameError:
        level = os.getenv("DECO_DEBUG_LEVEL")
        if not level:
            level = -1
        try:
            level = int(level)
        except TypeError:
            log.message("An invalid level number was used - must be an integer. Debug info will not be output")
            level = -1
        GLOBAL_DEBUG_LEVEL = level
        return GLOBAL_DEBUG_LEVEL
