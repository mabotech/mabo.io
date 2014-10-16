from flask import Flask, jsonify, render_template, request

from flask.helpers import make_response

from flask import Flask

import serial
import time 

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World!'
    
    
if __name__ == '__main__':
    app.debug = True
    app.run(host="127.0.0.1", port="6226")    