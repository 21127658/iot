import serial
import threading
import flask
from flask import render_template
import time
import datetime

def readingThread():
    global is_reading
    with serial.Serial('COM7', 9600, timeout = 2) as ser:
        while is_reading:
            line = ser.readline()
            update_data(line.strip())
        ser.close()

def update_data(s):
    global data
    named_tuple = time.localtime() # get struct_time
    time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
    try:
        data = time_string + " (Brightness | Temperature(oC) | Humidity(%)): " + str(s)[2:-1]
        return True
    except ValueError:
        print("Invalid data: ", s)
        return False

app = flask.Flask(__name__)

@app.route('/')
def auto():
    global data
    return data

# Turn off serial monitor on Arduino IDE before running this script
if __name__ == '__main__':
    tmp = 1
    global is_reading 
    is_reading = True
    global data
    data = ""
    t = threading.Thread(target=readingThread)
    t.start()
    app.run(host='0.0.0.0')
    while True:
        if tmp > 100:
            is_reading = False
            break
        tmp += 1
