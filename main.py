from flask import Flask, render_template, Response
import cv2
import numpy as np
import pyautogui

app = Flask(__name__)


def gen_frames():  # generate frame by frame from camera
    while True:
        # Take screenshot using PyAutoGUI
        img = pyautogui.screenshot()

        # Convert the screenshot to a numpy array
        frame = np.array(img)

        # Convert it from BGR(Blue, Green, Red) to
        # RGB(Red, Green, Blue)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


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
