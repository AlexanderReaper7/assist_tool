# Does screen capture and saves to rgba8 image
import cv2
import numpy as np

def setup_screen_capturer():
    s = cv2.getDesktopDisplayName()
    screen = cv2.VideoCapture(0)

    # Get screen sizepy
    _, frame = screen.read()
    screen_width, screen_height = frame.shape[1], frame.shape[0]
    print("Screen resolution: %s x %s" % (screen_width, screen_height))

    # Select region of interest
    x1 = 0
    y1 = 0
    x2 = 3840
    y2 = 2160

    # Capture screen
    screen.set(cv2.CAP_PROP_FRAME_WIDTH, x2 - x1)
    screen.set(cv2.CAP_PROP_FRAME_HEIGHT, y2 - y1)
    screen.set(cv2.CAP_PROP_POS_X, x1)
    screen.set(cv2.CAP_PROP_POS_Y, y1)  
    return screen

# Capture screen
def capture_screen(screen, filename):
    # Save screen
    _, frame = screen.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    if filename is not None:
        cv2.imwrite(filename, frame)
    else:
        cv2.imwrite("screenshot.png", frame)

def release_screen_capturer(screen):
    # Release screen
    screen.release()
    cv2.destroyAllWindows()