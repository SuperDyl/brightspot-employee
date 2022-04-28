import re


class Room:
    def __init__(self, building, floor, rm_num, rm_letter=''):
        self.floor = floor
        self.rm_num = rm_num
        self.rm_letter = rm_letter
        self.building = building

    def __str__(self):
        output = ''
        if self.floor:
            output += f'{self.floor}f'
        if self.rm_num:
            output += f' {self.rm_num}{self.rm_letter}'
        if self.building:
            output += f' {self.building}'
        return output.strip()

    def __repr__(self):
        return str(self)

    def __bool__(self):
        return any((self.building, self.floor, self.rm_num))

    @staticmethod
    def _clean_string(string):
        clean_string = string.strip()
        clean_string = re.sub(r'-', ' ', clean_string)
        clean_string = re.sub(r'Office(:\s)*', '', clean_string)
        clean_string = re.sub(r'Joseph.*', 'JSB', clean_string)
        clean_string = re.sub(r'Heber.*', 'HGB', clean_string)
        clean_string = re.sub(r'(?<=\d)\s*([^\d\s])(?!\w)', r'\g<1>', clean_string)
        return clean_string

    @staticmethod
    def _split_string(string):
        building = re.search(r'[^\d\s]{2,}', string)
        building = "" if not building else building.group(0)
        rm_num = re.search(r'\d{2,}', string)
        rm_num = "" if not rm_num else rm_num.group(0)
        rm_letter = re.search(r'(?<=\d{2})([^\d\s])(?!\w)', string)
        rm_letter = "" if not rm_letter else rm_letter.group(0)
        floor = rm_num[0] if rm_num else ""
        return building, floor, rm_num, rm_letter

    @classmethod
    def from_string(cls, string):
        string = Room._clean_string(string)
        return Room(*Room._split_string(string))

    @staticmethod
    def from_string_iter(string_iter):
        clean_string = '\n'.join(string_iter)
        # scrub data
        clean_string = Room._clean_string(clean_string)
        new_string_iter = clean_string.split('\n')
        # print(new_string_iter)

        return [Room(*Room._split_string(room_string))
                for room_string in new_string_iter]
