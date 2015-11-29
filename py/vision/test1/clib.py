
import sys

def report(message="", error=False):
    """ print message in multiprocessing script """
    message = str(message)
    
    if len(message) >= 70 and not error:
        message = message[:67] + "..."
    sys.stdout.write("\r{:70}{}".format(message, "\n" if error else ""))
    sys.stdout.flush()