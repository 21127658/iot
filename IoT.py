import serial
import threading
import flask
from flask import render_template

def readingThread():
    global is_reading
    with serial.Serial('COM7', 9600, timeout=1) as ser:
        while is_reading:
            line = ser.readline()
            update_data(line.strip())
            
def update_data(s):
    global data
    try:
        data = int(s)
        return True
    except:
        print("Invalid data: ", s)
        return False

app = flask.Flask(__name__)
@app.route('/')
def hello():
    return render_template('/templates/view.html')

state = 'initiate'
@app.route('/cmd', methods = ["GET"])
def cmd():
    global state
    new_state = flask.request.args.get('state')
    if new_state:
        state = new_state
    return f"<p><strong>State: {state}</strong></p>"

# Turn off serial monitor on Arduino IDE before running this script
if __name__ == '__main__':
    app.run(host = '0.0.0.0')
    global is_reading
    is_reading = True
    global data
    data = 0
    t = threading.Thread(target=readingThread)
    t.start()
    while True:
        print(data)
        if data > 100:
            is_reading = False
            break
    