
from flask import Flask, jsonify, render_template, request

from flask.helpers import make_response

from flask import Flask

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


    ser = serial.Serial('COM25',baudrate=9600,
    parity=serial.PARITY_NONE, #EVEN,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS, #SEVENBITS,
    timeout=0)  # open first serial port

    rawdata = ":MEAS:BATT?\r\n"
    
    ser.write(rawdata)      # write a string
    ser.flush()

    time.sleep(0.1)

    val = ser.readline() 

    v = request.args['callback']
    """
    jsonstr = '%s ({"name":"Super Hero","salutation":"Pryvitannie","greeting":"Pryvitannie Super Hero!"});' %(v)
    response = make_response(jsonstr)
    response.headers['Content-Type'] = 'application/javascript'
    response.headers['X-Pad'] = 'avoid browser bug' #X-Pad=avoid browser bug
    response.headers['Cache-Control'] = 'max-age=7200'

    response.headers['Vary'] = 'Accept-Encoding'

    return response
    """


 
    a = 1
    b = 3
    #app.logger.debug('A value for debugging:%s' %(a))
    jsons = jsonify(result=a + b,  s='xyz', a = [1,2,3], d1 = {'a1':'x', 'b1':'y'})
    #app.logger.debug(jsons)
    #return "JSON_CALLBACK (%s)" %(jsons.data)
    json = "dt = %s" % jsonify( batt = val ).data
    #val = "12,34,OFF"
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