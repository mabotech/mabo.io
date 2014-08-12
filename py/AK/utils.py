
import toml

def get_conf(conf_fn):
    
    """ get configuration from .toml"""
    
    
    with open(conf_fn) as conf_fh:
        
        conf = toml.loads(conf_fh.read())
        
        #print(config)
        return conf