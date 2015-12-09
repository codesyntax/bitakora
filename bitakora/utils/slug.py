from time import time

def time_slug():
    """ """
    return int(time())
    
def time_slug_long():
    """ """
    return int(time()*1000)

def time_slug_string():
    """ """
    return str(time_slug_long())