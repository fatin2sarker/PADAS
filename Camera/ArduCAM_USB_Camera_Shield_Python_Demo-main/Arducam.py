import threading  # Import threading module for concurrent execution
import ArducamSDK  # Import ArducamSDK for interacting with the camera
from utils import *  # Import custom utility functions from utils module

# Define a class for Arducam camera operations
class ArducamCamera(object):
    def __init__(self):
        self.isOpened = False  # Flag to indicate if the camera is opened
        self.running_ = False  # Flag to indicate if the camera is running
        self.signal_ = threading.Condition()  # Condition variable for synchronization

    # Method to open the camera
    def openCamera(self, fname, index=0):
        # Initialize the camera and obtain its configuration
        self.isOpened, self.handle, self.cameraCfg, self.color_mode = camera_initFromFile(fname, index)
        return self.isOpened

    # Method to start capturing images from the camera
    def start(self):
        if not self.isOpened:
            raise RuntimeError("The camera has not been opened.")  # Raise an error if the camera is not opened

        self.running_ = True  # Set the running flag to True
        # Set the camera mode to continuous capture
        ArducamSDK.Py_ArduCam_setMode(self.handle, ArducamSDK.CONTINUOUS_MODE)
        # Create and start a new thread for image capture
        self.capture_thread_ = threading.Thread(target=self.capture_thread)
        self.capture_thread_.daemon = True
        self.capture_thread_.start()

    # Method to read a captured image from the camera
    def read(self, timeout=1500):
        if not self.running_:
            raise RuntimeError("The camera is not running.")  # Raise an error if the camera is not running

        # Wait for an image to be available for a specified timeout period
        if ArducamSDK.Py_ArduCam_availableImage(self.handle) <= 0:
            with self.signal_:
                self.signal_.wait(timeout / 1000.0)

        # If no image is available after the timeout, return False
        if ArducamSDK.Py_ArduCam_availableImage(self.handle) <= 0:
            return (False, None, None)

        # Read the image data and configuration
        ret, data, cfg = ArducamSDK.Py_ArduCam_readImage(self.handle)
        ArducamSDK.Py_ArduCam_del(self.handle)  # Delete the image buffer
        size = cfg['u32Size']
        # If the image reading was unsuccessful, return False
        if ret != 0 or size == 0:
            return (False, data, cfg)
    
        return (True, data, cfg)  # Return True along with the image data and configuration

    # Method to stop capturing images from the camera
    def stop(self):
        if not self.running_:
            raise RuntimeError("The camera is not running.")  # Raise an error if the camera is not running

        self.running_ = False  # Set the running flag to False
        self.capture_thread_.join()  # Wait for the capture thread to finish

    # Method to close the camera
    def closeCamera(self):
        if not self.isOpened:
            raise RuntimeError("The camera has not been opened.")  # Raise an error if the camera is not opened

        if self.running_:
            self.stop()  # Stop capturing images if the camera is running
        self.isOpened = False  # Set the isOpened flag to False
        ArducamSDK.Py_ArduCam_close(self.handle)  # Close the camera handle
        self.handle = None  # Set the camera handle to None

    # Method to capture images in a separate thread
    def capture_thread(self):
        # Begin capturing images
        ret = ArducamSDK.Py_ArduCam_beginCaptureImage(self.handle)
        if ret != 0:
            self.running_ = False
            raise RuntimeError("Error beginning capture, Error : {}".format(GetErrorString(ret)))

        print("Capture began, Error : {}".format(GetErrorString(ret)))  # Print capture status
        
        # Continuously capture images while the camera is running
        while self.running_:
            ret = ArducamSDK.Py_ArduCam_captureImage(self.handle)
            if ret > 255:
                print("Error capture image, Error : {}".format(GetErrorString(ret)))
                if ret == ArducamSDK.USB_CAMERA_USB_TASK_ERROR:
                    break
            elif ret > 0:
                with self.signal_:
                    self.signal_.notify()  # Notify waiting threads when an image is captured
            
        self.running_ = False  # Set the running flag to False when capturing is stopped
        ArducamSDK.Py_ArduCam_endCaptureImage(self.handle)  # End image capturing

    # Method to set camera control parameters
    def setCtrl(self, func_name, val):
        return ArducamSDK.Py_ArduCam_setCtrl(self.handle, func_name, val)

    # Method to dump camera device information
    def dumpDeviceInfo(self):
        # Read information from the CPLD (Complex Programmable Logic Device)
        USB_CPLD_I2C_ADDRESS = 0x46
        cpld_info = {}
        # Read CPLD version and date
        ret, version = ArducamSDK.Py_ArduCam_readReg_8_8(self.handle, USB_CPLD_I2C_ADDRESS, 0x00)
        ret, year = ArducamSDK.Py_ArduCam_readReg_8_8(self.handle, USB_CPLD_I2C_ADDRESS, 0x05)
        ret, mouth = ArducamSDK.Py_ArduCam_readReg_8_8(self.handle, USB_CPLD_I2C_ADDRESS, 0x06)
        ret, day = ArducamSDK.Py_ArduCam_readReg_8_8(self.handle, USB_CPLD_I2C_ADDRESS, 0x07)
        cpld_info["version"] = "v{}.{}".format(version >> 4, version & 0x0F)
        cpld_info["year"] = year
        cpld_info["mouth"] = mouth
        cpld_info["day"] = day
        print(cpld_info)  # Print CPLD information

        # Read USB information
        ret, data = ArducamSDK.Py_ArduCam_getboardConfig(self.handle, 0x80, 0x00, 0x00, 2)
        usb_info = {}
        usb_info["fw_version"] = "v{}.{}".format((data[0] & 0xFF), (data[1] & 0xFF))
        usb_info["interface"] = 2 if self.cameraCfg["usbType"] == 4 else 3
        usb_info["device"] = 3 if self.cameraCfg["usbType"] == 3 or self.cameraCfg["usbType"] == 4 else 2
        print(usb_info)  # Print USB information

    # Method to get camera information
    def getCamInformation(self):
        # Read camera information from the CPLD
        self.version = ArducamSDK.Py_ArduCam_readReg_8_8(self.handle, 0x46, 00)[1]
        self.year = ArducamSDK.Py_ArduCam_readReg_8_8(self.handle, 0x46, 5)[1]
        self.mouth = ArducamSDK.Py_ArduCam_readReg_8_8(self.handle, 0x46, 6)[1]
        self.day = ArducamSDK.Py_ArduCam_readReg_8_8(self.handle, 0x46, 7)[1]
        cpldVersion = "V{:d}.{:d}\t20{:0>2d}/{:0>2d}/{:0>2d}".format(self.version >> 4, self.version & 0x0F, self.year,
                                                                    self.mouth, self.day)
        return cpldVersion  # Return formatted CPLD version information

    # Method to get MIPI data information
    def getMipiDataInfo(self):
        # Initialize MIPI data dictionary
        mipiData = {"mipiDataID": "",
                    "mipiDataRow": "",
                    "mipiDataCol": "",
                    "mipiDataClk": "",
                    "mipiWordCount": "",
                    "mFramerateValue": ""}
        # Read camera information from the CPLD
        self.getCamInformation()
        cpld_version = self.version & 0xF0
        date = (self.year * 1000 + self.mouth * 100 + self.day)

        # Check CPLD version and date for compatibility
        if cpld_version not in [0x20, 0x30]:
            return None
        if cpld_version == 0x20 and date < (19 * 1000 + 7 * 100 + 8):
            return None
        elif cpld_version == 0x30 and date < (19 * 1000 + 3 * 100 + 22):
            return None

        # Read MIPI data information from registers
        mipiDataID = ArducamSDK.Py_ArduCam_readReg_8_8(self.handle, 0x46, 0x1E)[1]
        mipiData["mipiDataID"] = hex(mipiDataID)

        rowMSB = ArducamSDK.Py_ArduCam_readReg_8_8(self.handle, 0x46, 0x21)[1]
        rowLSB = ArducamSDK.Py_ArduCam_readReg_8_8(self.handle, 0x46, 0x22)[1]
        mipiDataRow = ((rowMSB & 0xFF) << 8) | (rowLSB & 0xFF)
        mipiData["mipiDataRow"] = str(mipiDataRow)

        colMSB = ArducamSDK.Py_ArduCam_readReg_8_8(self.handle, 0x46, 0x1F)[1]
        colLSB = ArducamSDK.Py_ArduCam_readReg_8_8(self.handle, 0x46, 0x20)[1]
        mipiDataCol = ((colMSB & 0xFF) << 8) | (colLSB & 0xFF)
        mipiData["mipiDataCol"] = str(mipiDataCol)

        if cpld_version == 0x20 and date < (20 * 1000 + 6 * 100 + 22):
            return mipiData
        elif cpld_version == 0x30 and date < (20 * 1000 + 6 * 100 + 22):
            return mipiData

        mipiDataClk = ArducamSDK.Py_ArduCam_readReg_8_8(self.handle, 0x46, 0x27)[1]
        mipiData["mipiDataClk"] = str(mipiDataClk)

        if (cpld_version == 0x30 and date >= (21 * 1000 + 3 * 100 + 1)) or (
                cpld_version == 0x20 and date >= (21 * 1000 + 9 * 100 + 6)):
            wordCountMSB = ArducamSDK.Py_ArduCam_readReg_8_8(self.handle, 0x46, 0x25)[1]
            wordCountLSB = ArducamSDK.Py_ArduCam_readReg_8_8(self.handle, 0x46, 0x26)[1]
            mipiWordCount = ((wordCountMSB & 0xFF) << 8) | (wordCountLSB & 0xFF)
            mipiData["mipiWordCount"] = str(mipiWordCount)

        if date >= (21 * 1000 + 6 * 100 + 22):
            fpsMSB = ArducamSDK.Py_ArduCam_readReg_8_8(self.handle, 0x46, 0x2A)[1]
            fpsLSB = ArducamSDK.Py_ArduCam_readReg_8_8(self.handle, 0x46, 0x2B)[1]
            fps = (fpsMSB << 8 | fpsLSB) / 4.0
            fpsResult = "{:.1f}".format(fps)
            mipiData["mFramerateValue"] = fpsResult
        return mipiData  # Return MIPI data information dictionary