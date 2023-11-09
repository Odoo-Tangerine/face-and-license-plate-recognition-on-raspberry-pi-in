import cv2
import numpy as np
import face_recognition
from dataclasses import dataclass


@dataclass
class FaceRecognition:

    @staticmethod
    def _resize_image_to_1_4(frame):
        return cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    @staticmethod
    def _face_locations(small_frame):
        return face_recognition.face_locations(small_frame)

    @staticmethod
    def _face_encodings(small_frame, locations):
        return face_recognition.face_encodings(small_frame, locations)

    @staticmethod
    def _compare_faces(known_face_encodings, face_encoding):
        return face_recognition.compare_faces(known_face_encodings, face_encoding)

    @staticmethod
    def _face_distance(known_face_encodings, face_encoding):
        return face_recognition.face_distance(known_face_encodings, face_encoding)

    def handle_face_recognition(self, frame, known_face_encodings):
        face_locations = self._face_locations(self._resize_image_to_1_4(frame))
        if not face_locations:
            return False
        face_encodings = self._face_encodings(self._resize_image_to_1_4(frame), face_locations)
        for face_encoding in face_encodings:
            matches = self._compare_faces(known_face_encodings, face_encoding)
            face_distances = self._face_distance(known_face_encodings, face_encoding)
            match_index = np.argmin(face_distances)
            return matches[match_index]