from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from picamera2 import Picamera2
import io

app = FastAPI()

picam = Picamera2()
picam.configure(picam.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
picam.start()

def generate_frames():
    while True:
        im = picam.capture_array()
        with io.BytesIO() as buf:
            picam.capture_file(buf, format='jpeg')
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buf.getvalue() + b'\r\n')

@app.get("/video_feed")
async def video_feed():
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

@app.get("/")
async def root():
    return {"message": "Welcome to the Raspberry Pi camera stream!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
