import argparse
import time
import signal
import cv2

from Arducam import *
from ImageConvert import *


#importing some useful packages
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import sklearn.linear_model as sk_lin_mod
import sklearn.datasets as sk_data


# Import everything needed to edit/save/watch video clips
from moviepy.editor import VideoFileClip
from IPython.display import HTML

def grayscale(img):
    """Applies the Grayscale transform
    This will return an image with only one color channel
    but NOTE: to see the returned image as grayscale
    (assuming your grayscaled image is called 'gray')
    you should call plt.imshow(gray, cmap='gray')"""
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # Or use BGR2GRAY if you read an image with cv2.imread()
    # return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
def canny(img, low_threshold, high_threshold):
    """Applies the Canny transform"""
    return cv2.Canny(img, low_threshold, high_threshold)

def gaussian_blur(img, kernel_size):
    """Applies a Gaussian Noise kernel"""
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

def region_of_interest(img, vertices):
    """
    Applies an image mask.
    
    Only keeps the region of the image defined by the polygon
    formed from `vertices`. The rest of the image is set to black.
    `vertices` should be a numpy array of integer points.
    """
    #defining a blank mask to start with
    mask = np.zeros_like(img)   
    
    #defining a 3 channel or 1 channel color to fill the mask with depending on the input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255
        
    #filling pixels inside the polygon defined by "vertices" with the fill color    
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    
    #returning the image only where mask pixels are nonzero
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

# def draw_lines(img, lines, color=[255, 0, 0], thickness=2):
#     """
#     NOTE: this is the function you might want to use as a starting point once you want to 
#     average/extrapolate the line segments you detect to map out the full
#     extent of the lane (going from the result shown in raw-lines-example.mp4
#     to that shown in P1_example.mp4).  
    
#     Think about things like separating line segments by their 
#     slope ((y2-y1)/(x2-x1)) to decide which segments are part of the left
#     line vs. the right line.  Then, you can average the position of each of 
#     the lines and extrapolate to the top and bottom of the lane.
    
#     This function draws `lines` with `color` and `thickness`.    
#     Lines are drawn on the image inplace (mutates the image).
#     If you want to make the lines semi-transparent, think about combining
#     this function with the weighted_img() function below
#     """
#     for line in lines:
#         for x1,y1,x2,y2 in line:
#             cv2.line(img, (x1, y1), (x2, y2), color, thickness)

def draw_lines(img, lines, color=[255, 0, 0], thickness=2):
    """
    NOTE: this is the function you might want to use as a starting point once you want to 
    average/extrapolate the line segments you detect to map out the full
    extent of the lane (going from the result shown in raw-lines-example.mp4
    to that shown in P1_example.mp4).  
    
    Think about things like separating line segments by their 
    slope ((y2-y1)/(x2-x1)) to decide which segments are part of the left
    line vs. the right line.  Then, you can average the position of each of 
    the lines and extrapolate to the top and bottom of the lane.
    
    This function draws `lines` with `color` and `thickness`.    
    Lines are drawn on the image inplace (mutates the image).
    If you want to make the lines semi-transparent, think about combining
    this function with the weighted_img() function below
    """

    # LINE SEGMENT CLASSIFICATION
    left_x = []
    left_y = []
    right_x = []
    right_y = []
    if lines is not None:
        for line in lines:
            line_arr = line[0]
            if (line_arr[3] - line_arr[1]) < 0 and line_arr[2] < 480 and line_arr[0] < 480:
                left_x.append(np.array([line_arr[0]]))
                left_y.append(np.array([line_arr[1]]))
                left_x.append(np.array([line_arr[2]]))
                left_y.append(np.array([line_arr[3]]))
            elif (line_arr[3] - line_arr[1]) >= 0 and line_arr[2] >= 480 and line_arr[0] >= 480:
                right_x.append(np.array([line_arr[0]]))
                right_y.append(np.array([line_arr[1]]))
                right_x.append(np.array([line_arr[2]]))
                right_y.append(np.array([line_arr[3]]))
        
        # LINE FITTING
        if len(left_x) > 0:
            ransac_left = sk_lin_mod.RANSACRegressor(sk_lin_mod.LinearRegression(), max_trials=500, min_samples=2, residual_threshold=10,stop_n_inliers=50)
            ransac_left.fit(left_y, left_x)
            prediction_left = ransac_left.predict([np.array([540]), np.array([350])])
            if prediction_left[1][0] < prediction_left[0][0]:
                print(ransac_left.score(left_y, left_x))
                print(left_x)
                print(left_y)
            cv2.line(img, (int(prediction_left[0][0]), 540), (int(prediction_left[1][0]), 350), color=[255, 0, 0], thickness=10)

        if len(right_x) > 0:
            ransac_right = sk_lin_mod.RANSACRegressor(sk_lin_mod.LinearRegression(), max_trials=500, min_samples=2, residual_threshold=10,stop_n_inliers=50)
            ransac_right.fit(right_y, right_x)
            prediction_right = ransac_right.predict([np.array([540]), np.array([350])])
            cv2.line(img, (int(prediction_right[0][0]), 540), (int(prediction_right[1][0]), 350), color=[255, 0, 0], thickness=10)
        
        # LANE CENTERING TEXT PROMPT
        screen_width = 960 # CHANGE DEPENDING ON SCREEN RESOLUTION WIDTH
        screen_text = ""
        if len(left_x) > 0 and len(right_x) > 0:
            front_length = prediction_right[1][0] - prediction_left[1][0]
            back_length = prediction_right[0][0] - prediction_left[0][0]
            front_length_scale = 3.3/front_length # CHANGE TO SCALE TO REAL LANE WIDTH
            back_length_scale = 3.3/back_length # CHANGE TO SCALE TO REAL LANE WIDTH
            center_x_front = front_length/2 + prediction_left[1][0]
            center_x_back = back_length/2 + prediction_left[0][0]
            center_diff_front = screen_width/2 - center_x_front
            center_diff_back = screen_width/2 - center_x_back
            center_diff_front_meters = center_diff_front*front_length_scale
            center_diff_back_meters = center_diff_back*back_length_scale 
            center_diff_meters = (center_diff_front_meters + center_diff_back_meters)/2

            if center_diff_meters > 0:
                screen_text = "Steer RIGHT " + str(round(abs(center_diff_meters),4)) + " meters."
            elif center_diff_meters < 0:
                screen_text = "Steer LEFT " + str(round(abs(center_diff_meters),4)) + " meters."
            else:
                screen_text = "Fully Centered!"

            org = (50, 50)
            font = cv2.FONT_HERSHEY_COMPLEX
            color = (255,255,255)
            fontScale = 1
            thickness = 2
            lineType = cv2.LINE_AA
            bottomLeftOrigin = False
            
            cv2.putText(img, screen_text, org, font, fontScale, color, thickness, lineType, bottomLeftOrigin)



def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
    """
    `img` should be the output of a Canny transform.
        
    Returns an image with hough lines drawn.
    """
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    draw_lines(line_img, lines)
    
    return line_img

# Python 3 has support for cool math symbols.

def weighted_img(img, initial_img, α=0.8, β=1., γ=0.):
    """
    `img` is the output of the hough_lines(), An image with lines drawn on it.
    Should be a blank image (all black) with lines drawn on it.
    
    `initial_img` should be the image before any processing.
    
    The result image is computed as follows:
    
    initial_img * α + img * β + γ
    NOTE: initial_img and img must be the same shape!
    """
    return cv2.addWeighted(initial_img, α, img, β, γ)


def process_image(image):
    # NOTE: The output you return should be a color image (3 channel) for processing video below
    # TODO: put your pipeline here,
    # you should return the final output (image where lines are drawn on lanes)

    # COLOR THRESHOLDING
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # mask_yellow = cv2.inRange(hsv, (80, 70, 100), (110, 255, 255))
    mask_white = cv2.inRange(hsv, (0, 0, 200), (255, 20, 255))

    # final_color_mask = cv2.bitwise_or(mask_yellow, mask_white)
    color_threshold_out = cv2.bitwise_and(image, image, mask=mask_white)

    # CONVERSION TO GRAYSCALE
    gray_image = cv2.cvtColor(color_threshold_out, cv2.COLOR_BGR2GRAY)

    # GAUSSIAN SMOOTHING
    kernel_size = 3
    gaussian_blur_image = gaussian_blur(gray_image, kernel_size)

    # CANNY EDGE DETECTOR
    canny_lower = 200
    canny_higher = 600
    canny_image = canny(gaussian_blur_image, canny_lower, canny_higher)

    # REGION OF INTEREST SELECTION
    roi_vertices = [np.array([np.array([100,520]),np.array([950,520]),np.array([650,350]),np.array([350,350])])]
    roi_image = region_of_interest(canny_image, roi_vertices)

    # LINE SEGMENT DETECTION
    line_seg_image = hough_lines(canny_image, 1, np.pi/180, 5, 0, 250)
    
    result = weighted_img(line_seg_image, image, α=0.8, β=1., γ=0.)
    return result






# CAMERA CODE (COPIED FROM DEMO)

exit_ = False


def sigint_handler(signum, frame):
    global exit_
    exit_ = True


signal.signal(signal.SIGINT, sigint_handler)
signal.signal(signal.SIGTERM, sigint_handler)


def display_fps(index):
    display_fps.frame_count += 1

    current = time.time()
    if current - display_fps.start >= 1:
        print("fps: {}".format(display_fps.frame_count))
        display_fps.frame_count = 0
        display_fps.start = current


display_fps.start = time.time()
display_fps.frame_count = 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--config-file', type=str, required=True, help='Specifies the configuration file.')
    parser.add_argument('-v', '--verbose', action='store_true', required=False, help='Output device information.')
    parser.add_argument('--preview-width', type=int, required=False, default=-1, help='Set the display width')
    parser.add_argument('-n', '--nopreview', action='store_true', required=False, help='Disable preview windows.')
    

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

            processed_image = process_image(image) # ADD FILTERS ONTO CAMERA FOOTAGE (DOESNT WORK CURRENTLY)
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


# white_output = 'test_videos_output/solidWhiteRight.mp4'
# ## To speed up the testing process you may want to try your pipeline on a shorter subclip of the video
# ## To do so add .subclip(start_second,end_second) to the end of the line below
# ## Where start_second and end_second are integer values representing the start and end of the subclip
# ## You may also uncomment the following line for a subclip of the first 5 seconds
# # clip1 = VideoFileClip("test_videos/solidWhiteRight.mp4").subclip(0,5)
# clip1 = VideoFileClip("test_videos/solidWhiteRight.mp4")
# white_clip = clip1.fl_image(process_image) #NOTE: this function expects color images!!
# white_clip.write_videofile(white_output, audio=False)
# # white_clip.write_videofile(white_output, audio=False)