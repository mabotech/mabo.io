
from flask import Flask, jsonify, render_template, request

from flask.helpers import make_response

from flask import Flask

import redis

from redis import Redis

import serial
import time 

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World!'
    
@app.route('/abc/')
#different function name
def hello_world2():
    return 'Hello World, abc!'    
    
@app.route('/json')
def json():


    ser = serial.Serial('COM12',baudrate=9600,
    parity=serial.PARITY_EVEN,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS, #SEVENBITS,
    timeout=0)  # open first serial port
    rawdata = "M:000"
    #ser.write(rawdata)
    val = ser.readline() 
    ser.close()
    v = request.args['callback']

    return "%s (%s);" %  (v, jsonify( batt = val).data)
    
 
@app.route('/welding')
def welding():
    
    pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
    
    rc = redis.Redis(connection_pool=pool)
    
    v = request.args['callback']
    
    val = rc.rpop('welding2')
    
    return "%s (%s);" %  (v, jsonify( batt = val).data)
    
    
    
@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id    

if __name__ == '__main__':
    
    app.debug = True
    app.run()
