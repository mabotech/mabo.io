# -*- coding: utf-8 -*-


LOGGING =  {
    'version': 1,              
    #'disable_existing_loggers': True,
    
    'formatters': {
        'verbose': {
            'format': '%(asctime)s [%(levelname)s] %(process)d, %(thread)d, %(name)s, %(module)s:%(lineno)s:%(message)s'
        },
        
        'performance': {
            'format': '%(asctime)s [%(levelname)s] %(process)d, %(thread)d, %(message)s'
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
                'backupCount':17 # total
            },            
            
        'debug': {
                'level':'DEBUG',    
                'class':'logging.handlers.RotatingFileHandler',
                'formatter':'verbose',
                'filename':'debug.log',
                'maxBytes':10240000,
                'backupCount':17
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
                'backupCount':17
            },   
            'error': {
                'level':'ERROR',    
                'class':'logging.handlers.RotatingFileHandler',
                'formatter':'verbose',
                'filename':'error.log',
                'maxBytes':10240000,
                'backupCount':17
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
