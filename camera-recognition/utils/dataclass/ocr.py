import re
from typing import List
from dataclasses import dataclass
from easyocr import Reader


@dataclass
class OCR:
    reader: Reader = Reader(['en'])

    @staticmethod
    def clean_character(text):
        character_cleaned = re.sub(r'[^\w\s]', '', text)
        character_cleaned = re.sub(r'\s', '', character_cleaned)
        return character_cleaned

    @staticmethod
    def _validate_license_plate_character(result):
        if not result or \
                len(result) != 2 or \
                not result[0][:2].isnumeric() or \
                not result[0][-1].isalpha() or \
                len(result[1]) not in [4, 5] or \
                not result[1].isnumeric():
            return False
        return True

    def extract_license_plate(self, threshold_image):
        results = self.reader.readtext(threshold_image)
        character_lst = [self.clean_character(character) for _, character, score in results]
        is_valid = self._validate_license_plate_character(character_lst)
        if not is_valid:
            return False
        return ''.join(character_lst).upper()
