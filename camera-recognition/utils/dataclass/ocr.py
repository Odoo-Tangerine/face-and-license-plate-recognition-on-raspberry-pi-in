import re
from numpy import nparray
from typing import List
from dataclasses import dataclass
from easyocr import Reader


@dataclass
class OCR:
    reader: Reader = Reader(['en'])

    @staticmethod
    def clean_character(character):
        character_cleaned = re.sub(r'[^\w\s]', '', character)
        character_cleaned = re.sub(r'\s', '', character_cleaned)
        return character_cleaned

    @staticmethod
    def _validate_license_plate_character(character_lst: List[str]) -> bool:
        if not character_lst or \
            len(character_lst) != 2 or \
            not character_lst[0][:2].isnumeric() or \
            not character_lst[0][-1].isalpha() or \
            len(character_lst[1]) not in [4, 5] or \
            not character_lst[1].isnumeric():
            return False
        return True

    def extract_character(self, threshold_image: nparray):
        results = self.reader.readtext(threshold_image)
        character_lst = [self.clean_character(character) for _, character, score in results]
        is_valid = self._validate_license_plate_character(character_lst)
        if not is_valid:
            return False
        return ''.join(character_lst).upper()