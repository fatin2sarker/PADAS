from ultralytics import YOLO
from PIL import Image
#from Arducam import*


#def detect(x):
# New Model used
model = YOLO("yolov8m.pt")

# Use Model to detect traffic light through camera image
results = model.predict("3_crosswalk.jpg")
output = results[0]

# Number of Objects Detected
number = len(output.boxes)
print("Number of Objects Detected:", number)

# For Loop that goes through and pulls info for traffic light detected
for box in output.boxes:
    name = output.names[box.cls[0].item()]
    coordinates = [round(x) for x in box.xyxy[0].tolist()]
    probability = box.conf[0].item()
    if probability >= 0.9:
        print("ALERT: Brake", name, "in front of you!")
        print("Object Name:", name)
        print("Coordinates:", coordinates)
        print("Probability", probability)
    '''print("Object Name:", name)
    print("Coordinates:", coordinates)
    print("Probability", probability)
    if name == "green_light":
        print("ALERT: GO Green Light")
    elif name == "yellow_light":
        print("ALERT: SLOW DOWN Yellow Light")
    elif name == "red_light":
        print("ALERT: STOP Red Light")'''

# Displays detected objects in image
img = (Image.fromarray(output.plot()[:, :, ::-1]))
img.show()
'''return img

args = parser.parse_args()
config_file = args.config_file
verbose = args.verbose
preview_width = args.preview_width
no_preview = args.nopreview

camera = ArducamCamera()

if not camera.openCamera(config_file):
    raise RuntimeError("Failed to open camera.")

if verbose:
    camera.dumpDeviceInfo()

camera.start()
camera.setCtrl("setFramerate", 40)
# camera.setCtrl("setExposureTime", 20000)
# camera.setCtrl("setAnalogueGain", 800)

scale_width = preview_width

while not exit_:
    ret, data, cfg = camera.read()

    display_fps(0)

    if no_preview:
        continue

    if ret:
        image = convert_image(data, cfg, camera.color_mode)

        if scale_width != -1:
            scale = scale_width / image.shape[1]
            image = cv2.resize(image, None, fx=scale, fy=scale)

        processed_image = detect(cfg)  # ADD FILTERS ONTO CAMERA FOOTAGE (DOESNT WORK CURRENTLY)
        cv2.imshow("Arducam", processed_image)
    else:
        print("timeout")

    key = cv2.waitKey(1)
    if key == ord('q'):
        exit_ = True
    elif key == ord('s'):
        np.array(data, dtype=np.uint8).tofile("processedimage.raw")
        print("pressed s")

camera.stop()
camera.closeCamera()
#.convert('L'))
#box = result.boxes[0]
print("Object type:", box.cls)
print("Coordinates:", box.xyxy)
print("Probability", box.conf)'''

# Train YOLO with Traffic Light Dataset
#model.train(data="data.yaml",epochs=1)
# If Statement that alerts driver if object is in front of car'''
