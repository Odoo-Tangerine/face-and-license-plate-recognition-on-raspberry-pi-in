import asyncio
from numpy import nparray
from typing import List, Any
from api.odoo_api import OdooAPI
from dataclasses import dataclass
from utils.dataclass.ocr import OCR
from database.postgresql import Postgres
from utils.dataclass.face_recognition import FaceRecognition
from utils.dataclass.picamera import PiCamera
from utils.dataclass.yolo import LicensePlateRecognition


@dataclass
class ValidationIntoParking:
    ocr: OCR = OCR()
    odoo_api = OdooAPI()
    psql: Postgres = Postgres()
    picam: PiCamera = PiCamera()
    fr: FaceRecognition = FaceRecognition()
    lpr: LicensePlateRecognition = LicensePlateRecognition()

    def _request_authenticate_into_parking_lot(self, license_plate: str):
        return asyncio.run(self.odoo_api.authenticate_into_parking(license_plate))

    def into_parking_lot_authentication(self):
        frame = self.picam.picamera.capture_array()
        lp_img = self.lpr.recognition(frame)
        if not lp_img:
            return False
        lp_character = self.ocr.extract_character(lp_img)
        if not lp_character:
            return False
        data = self._request_authenticate_into_parking_lot(lp_character)
        return self.fr.handle_face_recognition(frame, data['face_encodings'])


if __name__ == '__main__':
    vlp = ValidationIntoParking()

    while True:
        is_valid = vlp.into_parking_lot_authentication()
        # Resize frame of video to 1/4 size for faster face recognition processing
        # small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        # face_locations = face_recognition.face_locations(small_frame)
        # face_encodings = face_recognition.face_encodings(small_frame, face_locations)