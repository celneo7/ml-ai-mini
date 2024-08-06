import cv2
import numpy as np
import mss

def process_frame(frame):
    # Implement your frame processing logic here
    return frame  # Return processed frame

# Create a named window
cv2.namedWindow('Processed Frame', cv2.WINDOW_NORMAL)

with mss.mss() as sct:
    monitor = {"top": 160, "left": 160, "width": 800, "height": 600}

    while True:
        img = np.array(sct.grab(monitor))
        frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        processed_frame = process_frame(frame)

        # Display the processed frame in the named window
        cv2.imshow('Processed Frame', processed_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Cleanup: close the window and release system resources
cv2.destroyAllWindows()
