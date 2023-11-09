import cv2
from dataclasses import dataclass
from numpy import nparray
from ultralytics import YOLO
from typing import Any


@dataclass
class LicensePlateRecognition:
    lp_model: YOLO = YOLO('./models/best.pt')

    def recognition(self, frame: nparray) -> Any:
        license_plates = self.lp_model(frame)[0]
        license_plate_lst = license_plates.boxes.data.tolist()
        if not license_plate_lst:
            return False
        for license_plate in license_plate_lst:
            x1, y1, x2, y2, yolo_score, class_id = license_plate
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)
            # crop license plate
            license_plate_cropped = frame[int(y1):int(y2), int(x1): int(x2), :]
            # blurred image
            img_blurred = cv2.GaussianBlur(license_plate_cropped, (5, 5), 0)
            # threshold blur image
            _, img_threshold = cv2.threshold(img_blurred, 64, 255, cv2.THRESH_BINARY_INV)
            return img_threshold