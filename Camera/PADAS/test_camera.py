import cv2
import time
from ArducamSDK import *

# Load the configuration file
config_file = ".\Config\USB2.0_UC-980_Rev.B\MIPI\OV9281\OV9281_MIPI_2Lane_RAW8_1280x800_90MHz.cfg"

# Initialize the camera
camera_instance = arducam_init_camera(config_file.encode("ascii"))

# Check if the camera is initialized successfully
if camera_instance.contents == None:
    print("Failed to initialize the camera")
    exit(1)

# Start the camera capture
if not arducam_start_capture(camera_instance):
    print("Failed to start capture")
    arducam_deinit_camera(camera_instance)
    exit(1)

try:
    # Main loop for capturing and processing frames
    while True:
        # Capture a frame from the camera
        frame = arducam_capture_image(camera_instance)

        # Convert the frame to a format compatible with OpenCV
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Perform lane detection (replace this with your actual lane detection algorithm)
        # Example: lane_detection_result = detect_lanes(frame)

        # Display the processed frame
        cv2.imshow("Lane Detection", frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Introduce a delay to control the frame rate
        time.sleep(0.1)

finally:
    # Release resources
    arducam_stop_capture(camera_instance)
    arducam_deinit_camera(camera_instance)
    cv2.destroyAllWindows()
