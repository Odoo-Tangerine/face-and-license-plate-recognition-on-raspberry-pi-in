from picamera2 import Picamera2
from dataclasses import dataclass


@dataclass
class PiCamera:
    picamera: Picamera2 = Picamera2()

    def __post_init__(self):
        self.picamera.configure(
            self.picamera.create_preview_configuration(
                main={
                    "format": 'XRGB8888',
                    "size": (640, 480)
                }
            )
        )