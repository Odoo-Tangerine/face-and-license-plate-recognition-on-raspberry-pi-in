import cv2
import pickle
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

    def compare_face(self, face, frame):
        data_face = pickle.loads(face.encode('latin-1'))
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = self._resize_image_to_1_4(frame)
        # Find all the faces and face encodings in the current frame of video
        face_locations = self._face_locations(small_frame)
        face_encodings = self._face_encodings(small_frame, face_locations)

        if not face_encodings: return False

        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = self._compare_faces([data_face], face_encoding)
            # Or instead, use the known fcea with the smallest distance to the new face
            face_distances = self._face_distance([data_face], face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                return matches[best_match_index]
