
import logging
logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)

import time

import falcon
import json
 
from waitress import serve


class HekaEndPoint:
    
    def __init__(self):
        self.info = "info"   
    
    def on_post(self, req, resp):
        """Handles GET requests"""
        #print req.headers
        print req.stream.read().strip()
        resp.body = "OK"
        
def main():
 
    api = falcon.API()
    api.add_route('/heka', HekaEndPoint())   


    serve(api, host='0.0.0.0', port=6227, _quiet=False)


if __name__ == "__main__":
    main()