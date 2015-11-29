# -*- coding: utf-8 -*-


LOGGING =  {
    'version': 1,              
    #'disable_existing_loggers': True,
    
    'formatters': {
        'verbose': {
            'format': '%(asctime)s [%(process)d][%(levelname)s] %(module)s,%(funcName)s,%(lineno)s:%(message)s'
        }, #, %(thread)d, %(name)s,
        
        'performance': {
            'format': '%(asctime)s [%(process)d] [%(levelname)s] %(message)s'
        },
        
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    
    'handlers': {
        'console': {
            'level':'DEBUG',    
            'class':'logging.StreamHandler',
            'formatter':'verbose'
        },  
            
        'performance': {
                'level':'DEBUG',    
                'class':'logging.handlers.RotatingFileHandler',
                'formatter':'performance',
                'filename':'performance.log',
                'maxBytes':10240000, # 10M
                'backupCount':7 # total
            },            
            
        'debug': {
                'level':'DEBUG',    
                'class':'logging.handlers.RotatingFileHandler',
                'formatter':'verbose',
                'filename':'debug.log',
                'maxBytes':10240000,
                'backupCount':7
            },          
            'info': {
                'level':'INFO',    
                'class':'logging.handlers.RotatingFileHandler',
                'formatter':'verbose',
                'filename':'info.log',
                'maxBytes':10240000,
                'backupCount':7
            },   
            'warning': {
                'level':'WARNING',    
                'class':'logging.handlers.RotatingFileHandler',
                'formatter':'verbose',
                'filename':'warning.log',
                'maxBytes':10240000,
                'backupCount':7
            },   
            'error': {
                'level':'ERROR',    
                'class':'logging.handlers.RotatingFileHandler',
                'formatter':'verbose',
                'filename':'error.log',
                'maxBytes':10240000,
                'backupCount':7
            }, 
    },
    
    'loggers': {
    
        '': {                  
            'handlers': ['console', 'info', 'warning', 'error',  'debug'],
            'level': 'DEBUG',  
            'propagate': True  
        },
        
        'performance': {                  
            'handlers': ['console', 'performance'],        
            'level': 'DEBUG',  
            'propagate': True  
        }        
        
    }
}
