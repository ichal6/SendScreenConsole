import PIL
from flask import Flask, render_template, Response
import cv2
import numpy as np
import pyautogui
from pynput.mouse import Button, Controller
import time

app = Flask(__name__)


def gen_frames():  # generate frame by frame from camera
    mouse = Controller()
    cursor = load_cursor()
    while True:
        start = time.time()
        # Take screenshot using PyAutoGUI
        img = pyautogui.screenshot()

        c_mode = img.mode

        cursor_array = np.array(cursor)

        cursor = cursor.convert('RGBA')

        # cursor_RGB = cv2.cvtColor(cursor_array, cv2.COLOR_)

        img.paste(cursor, (0,0), mask=cursor)

        # Convert the screenshot to a numpy array
        frame = np.array(img)

        # Convert it from BGR(Blue, Green, Red) to
        # RGB(Red, Green, Blue)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mouse_position = mouse.position

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
        end = time.time()
        elapsed_time = end - start


def load_cursor():
    try:
        image = PIL.Image.open('cursors/arrow.gif')
        return image
    except Exception as e:
        print(e)

@app.route('/video_feed')
def video_feed():
    # Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


if __name__ == '__main__':
    host = '192.168.1.103'
    port = '5000'

    print("Ustawienia domyślne:", f'host = {host}', f'port = {port}')
    answer = input("Czy zmienić ustawienia? [T/N] ").lower()

    if answer == 'T':
        host = input("Proszę podać adres hosta: ")
        port = input("Proszę podać numer portu: ")

    app.run(host="192.168.1.103", port=5000, debug=False)
