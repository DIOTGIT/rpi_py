from flask import Flask, Response
from picamera2 import Picamera2
import cv2
import time

### You can donate at https://www.buymeacoffee.com/mmshilleh 

app = Flask(__name__)

camera = Picamera2()
resolution = (1024, 768)
camera.configure(camera.create_preview_configuration(main={"format": 'XRGB8888', "size": resolution}))
camera.start()

def generate_frames():
    prev_time = time.time()
    while True:
        frame = camera.capture_array()
        current_time = time.time()
        fps = 1.0 / (current_time - prev_time)
        prev_time = current_time

        # Put the FPS and resolution text on the frame
        cv2.putText(frame, f'FPS: {fps:.2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, f'Resolution: {resolution[0]}x{resolution[1]}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
