"""
Representation of a room on a college campus
"""
import re
from typing import Union, Iterable, List


class Room:
    """
    Represents the exact address of a room on a college campus

    """
    def __init__(self, building: str, floor: Union[str, int], rm_num: Union[str, int], rm_letter: str = ''):
        self.floor = floor
        self.rm_num = rm_num
        self.rm_letter = rm_letter
        self.building = building

    def __str__(self) -> str:
        output = ''
        if self.floor:
            output += f'{self.floor}f'
        if self.rm_num:
            output += f' {self.rm_num}{self.rm_letter}'
        if self.building:
            output += f' {self.building}'
        return output.strip()

    def __repr__(self) -> str:
        """Return the room_string representation of this instance"""
        return str(self)

    def __bool__(self) -> bool:
        """Return False if no building, floor, or rm_num is specified"""
        return any((self.building, self.floor, self.rm_num))

    @staticmethod
    def clean_room_string(room_string: str) -> str:
        """
        Return a cleaned-up room input_string
        """
        clean_string = room_string.strip()
        clean_string = re.sub(r'-', ' ', clean_string)
        clean_string = re.sub(r'Office(:\s)*', '', clean_string)
        clean_string = re.sub(r'Joseph.*', 'JSB', clean_string)
        clean_string = re.sub(r'Heber.*', 'HGB', clean_string)
        clean_string = re.sub(r'(?<=\d)\s*([^\d\s])(?!\w)', r'\g<1>', clean_string)
        return clean_string

    @staticmethod
    def split_room_string(room_string: str) -> (str, str, str, str):
        """
        Return all parts of a room address from room_string (in order of Room initialization).
        """
        building = re.search(r'[^\d\s]{2,}', room_string)
        building = '' if building is None else building.group(0)

        rm_num = re.search(r'\d{2,}', room_string)
        rm_num = '' if rm_num is None else rm_num.group(0)

        rm_letter = re.search(r'(?<=\d{2})([^\d\s])(?!\w)', room_string)
        rm_letter = '' if rm_letter is None else rm_letter.group(0)

        floor = rm_num[0] if rm_num else ''
        return building, floor, rm_num, rm_letter

    @classmethod
    def from_string(cls, room_string: str):
        """
        Return a Room instance after cleaning-up room_string.
        """
        string = Room.clean_room_string(room_string)
        return Room(*Room.split_room_string(string))

    @staticmethod
    def from_room_string_for_each(string_iter: Iterable[str]) -> List['Room']:
        """
        Return a list of Room instances.
        More optimized by only cleaning the input_string once
        """
        clean_string = '\n'.join(string_iter)
        # scrub data
        clean_string = Room.clean_room_string(clean_string)
        new_string_iter = clean_string.split('\n')

        return [Room(*Room.split_room_string(room_string))
                for room_string in new_string_iter]
