from picamera2 import Picamera2
import datetime

def capture_image():
    # Initialize the camera
    picam2 = Picamera2()
    picam2.start()

    # Generate a filename based on the current date and time
    filename = datetime.datetime.now().strftime("/py/image_%Y%m%d_%H%M%S.jpg")
    
    # Capture the image
    picam2.capture_file(filename)
    
    print(f"Image saved as {filename}")

    # Stop the camera
    picam2.stop()

if __name__ == "__main__":
    capture_image()
