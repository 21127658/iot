import queue
from tkinter import SE
import serial
import threading
import flask
from flask import render_template, request
import time
import datetime
import binascii

class Led:
    def __init__(self):
        self.queue = queue.Queue()
        self.finish = False
        if data[-1] == '1':
            self.state = True
        else:             
            self.state = False
        self.thread = threading.Thread(target=self.__run__)
        self.thread.start()
        
    def __run__(self):
        while not self.finish:
            if not self.queue.empty():
                self.state = self.queue.get()
                ser.write(str(self.state).encode())
                time.sleep(0.5)
            else:
                time.sleep(0.5)
                
    def update(self, state):
        self.queue.put(state)
        
ser = serial.Serial('COM3', 9600, timeout=1)

def readingThread():
    global is_reading
    while is_reading:
        line = ser.readline()
        update_data(line.strip())

def CRCCal(rdata):
    return binascii.crc32(rdata);

def update_data(s):
    global data
    global timeChange
    time_string = time.strftime("%H:%M:%S", time.localtime())
    s = s.split()
    try:
        if(len(s) == 6):      # Check if the data is not "changed" - to change the LED state
            received_data = [s[0].decode(), s[2].decode(), s[4].decode()]
            received_crc = [int(s[1]), int(s[3]), int(s[5])]
            calculated_crc = [CRCCal(s[0]), CRCCal(s[2]), CRCCal(s[4])]
            if (received_crc == calculated_crc):
                data = ' '.join(received_data)
            else:
                data = "Invalid data received"
            data = time_string + " (Brightness | Temperature(oC) | LED state): " + data
        else: 
            if led.state == False:
                st = "OFF"
            else:
                st = "ON"
            timeChange = "LED state changed to " + st + " at " + time_string
        return True
    except ValueError:
        print("Invalid data: ", s)
        return False

app = flask.Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        led.update(not led.state)
    return render_template('view.html', data=data)

@app.route('/auto')
def auto():
    return data

@app.route('/timeAtChange')
def timeAtChange():
    return timeChange

# Turn off serial monitor on Arduino IDE before running this script
if __name__ == '__main__':
    global is_reading
    is_reading = True
    global data
    data = ""
    global timeChange
    timeChange = ""
    t = threading.Thread(target=readingThread)
    t.start()
    while data == "": {}
    led = Led()
    app.run(host = '0.0.0.0')
