from room import Room  # TODO: make part of package
from tools import remove_prefix

from contextlib import suppress

NAME_SUFFIXES = ('jr.', 'iii', 'sr.')
NON_EXISTENT = ''


class Professor2:
    def __init__(self, tag):
        self.first_name, self.last_name = process_split_name(tag)
        self.room = process_room(tag)
        self.page_url = process_page_url(tag)
        self.telephone = process_telephone(tag)
        self.department = process_department(tag)
        self.job_title = process_job_title(tag)

    def __str__(self):
        return str(self.__dict__)


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
    with suppress(IndexError, AttributeError, TypeError):
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