import cv2
import asyncio
import logging
import asyncio
from utils.ocr import OCR
from ultralytics import YOLO
from picamera2 import Picamera2
from api.odoo_api import OdooAPI
from gpiozero import DistanceSensor, Servo
from utils.face_recognition import FaceRecognition

_logger = logging.getLogger(__name__)

DISTANCE = 0
SERVO = Servo(17)
IS_LOCKED_CAMERA: bool = False
HC_SR04 = DistanceSensor(trigger=18, echo=24)
MODEL = YOLO('models/best.pt')

def unlock_recognition():
    global IS_LOCKED_RECOGNITION
    IS_LOCKED_RECOGNITION = False


def lock_recognition():
    global IS_LOCKED_RECOGNITION
    IS_LOCKED_RECOGNITION = True


def get_distance():
    while True:
        global DISTANCE
        DISTANCE = round((HC_SR04.distance * 100), 2)
    

if __name__ == '__main__':
    ocr = OCR()
    odooapi = OdooAPI()
    face = FaceRecognition()
    picamera = Picamera2()
    picamera.configure(picamera.create_preview_configuration())    
    try:
        picamera.start()
        while True:
            if DISTANCE < 50.00: continue
            frame = picamera.capture_array()
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            license_plates = MODEL(frame, verbose=False)[0]
            if not license_plates: continue
            for license_plate in license_plates.boxes.data.tolist():
                x1, y1, x2, y2, lp_score, class_id = license_plate
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)
                if IS_LOCKED_CAMERA: continue
                if lp_score > 0.75:
                    license_plate_cropped = frame[int(y1):int(y2), int(x1): int(x2), :]
                    img_blurred = cv2.GaussianBlur(license_plate_cropped, (5, 5), 0)
                    _, img_threshold = cv2.threshold(img_blurred, 64, 255, cv2.THRESH_BINARY_INV)
                    trust_license_plate = ocr.extract_license_plate(img_threshold)
                    if not trust_license_plate: continue
                    lock_recognition()
                    data = asyncio.run(odooapi.authenticate_into_parking(trust_license_plate))
                    if not data: continue
                    is_equal = face.compare_face(data.get('face_encoding'), frame)
                    if not is_equal: continue
                    unlock_recognition()
    except Exception as e:
        _logger.exception(e)
    finally:
        picamera.close()
