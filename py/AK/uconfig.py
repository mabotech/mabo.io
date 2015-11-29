

"""
get config
"""

import toml

def get_config(conf_file):
    """ get config """    
    
    with open(conf_file,"r") as fileh:
        
        config = toml.loads(fileh.read())
        
        return config