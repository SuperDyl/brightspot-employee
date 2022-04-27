from room import Room  # TODO: make part of package
from tools import remove_prefix

from pandas import DataFrame, read_csv

from contextlib import suppress

NAME_SUFFIXES = ('jr.', 'iii', 'sr.')
NON_EXISTENT = ''


class Professor:
    def __init__(self, first_name, last_name, room, page_url, telephone, department, job_title):
        self.first_name = first_name
        self.last_name = last_name
        self.room = room
        self.page_url = page_url
        self.telephone = telephone
        self.department = department
        self.job_title = job_title

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self)

    count = 0

    @classmethod
    def from_html_tag(cls, tag):
        # nonlocal count
        Professor.count += 1
        if Professor.count >= 525:
            print(Professor.count)
        first_name, last_name = process_split_name(tag)
        return cls(first_name,
                   last_name,
                   process_room(tag),
                   process_page_url(tag),
                   process_telephone(tag),
                   process_department(tag),
                   process_job_title(tag))

    @classmethod
    def from_dict(cls, kwargs):
        room = kwargs.room if isinstance(kwargs.room, Room) else Room.from_string(kwargs.room)
        return cls(kwargs.first_name,
                   kwargs.last_name,
                   room,
                   kwargs.page_url,
                   kwargs.telephone,
                   kwargs.department,
                   kwargs.job_title)

    @staticmethod
    def to_csv(file_path, professors: iter) -> None:
        dataframe = DataFrame.from_records((p.__dict__ for p in professors))
        dataframe.to_csv(file_path)

    @staticmethod
    def from_csv(file_path) -> list:
        dataframe = read_csv(file_path, keep_default_na=False)
        return [Professor.from_dict(row) for row in dataframe.itertuples()]


def process_job_title(tag):
    job_title = tag.find(class_='PromoVerticalImage-jobTitle')
    if job_title is None:
        return NON_EXISTENT
    return job_title.text


def process_department(tag):
    department = tag.find(class_='PromoVerticalImage-groups')
    if department is None:
        return NON_EXISTENT
    return department.text


def process_telephone(tag):
    telephone_tag = tag.find(class_='PromoVerticalImage-phoneNumber')
    if telephone_tag is None:
        return NON_EXISTENT
    phone_ref = telephone_tag.find('a')['href']
    return remove_prefix(phone_ref, 'tel:')


def process_page_url(tag):
    return tag.find(class_="Link")['href']


def process_room(tag):
    with suppress(AttributeError):
        room_text = tag.find('p').text.strip()
        return Room.from_string(room_text)
    return Room('', '', '')  # TODO: should this return empty Room or None?


def process_first_name(tag):
    first_name, _ = process_split_name(tag)
    return first_name


def process_last_name(tag):
    _, last_name = process_split_name(tag)
    return last_name


def process_full_name(tag):
    return tag.find('a', attrs={'data-cms-ai': '0'})['aria-label'].replace(u'\xa0', u' ')


def process_split_name(tag) -> (str, str):
    full_name = process_full_name(tag)
    full_split_name = full_name.split(' ')
    if full_split_name[-1].lower() in NAME_SUFFIXES:
        *first, last = full_split_name[:-1]
        return ' '.join(first), ' '.join((last, full_split_name[-1]))
    # else
    *first, last = full_split_name
    return ' '.join(first), last
