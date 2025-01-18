from picamera2 import Picamera2, Preview
import datetime
from flask import Flask, send_file
import threading
import time

app = Flask(__name__)
latest_image = "/py/latest.jpg"

def capture_image():
    global latest_image
    picam2 = Picamera2()
    picam2.configure(picam2.create_still_configuration(main={"size": (1920, 1080)}))  # Set resolution to 1920x1080
    picam2.start()
    
    while True:
        filename = "/py/latest.jpg"
        picam2.capture_file(filename)
        latest_image = filename
        time.sleep(1)  # Capture an image every second

    picam2.stop()

@app.route('/pic.jpg')
def serve_image():
    return send_file(latest_image, mimetype='image/jpeg')

if __name__ == "__main__":
    # Start the image capture in a separate thread
    capture_thread = threading.Thread(target=capture_image)
    capture_thread.daemon = True
    capture_thread.start()
    
    # Start the Flask web server
    app.run(host='0.0.0.0', port=5000)
