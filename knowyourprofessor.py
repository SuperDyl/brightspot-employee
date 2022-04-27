# from flashcard_powerpoint import FlashcardPowerPoint
from oldprofessor import OldProfessor
# from room import Room

from bs4 import BeautifulSoup
import requests

# import re
from functools import partial

import professor
from tools import call_each  # ,  # remove_prefix

RELED_DIR_URL = 'https://religion.byu.edu/directory'
NAME_SUFFIXES = professor.NAME_SUFFIXES


def process_room(tag):
    return professor.process_room(tag)


def process_first_name(tag):
    return professor.process_first_name(tag)


def process_last_name(tag):
    return professor.process_last_name(tag)


def process_split_name(tag) -> (str, str):
    return professor.process_split_name(tag)


def process_full_name(tag):
    return professor.process_full_name(tag)


def process_page_url(tag):
    return professor.process_page_url(tag)


def process_telephone(tag):
    return professor.process_telephone(tag)


def process_department(tag):
    return professor.process_department(tag)


def process_job_title(tag):
    return professor.process_job_title(tag)


def create_professor(tag):
    name, room, page_url = call_each((process_full_name, process_room, process_page_url), tag)
    return OldProfessor(str(name), room, pic_url=page_url)


def create_professor2(url=RELED_DIR_URL):
    with requests.get(url) as request:
        html_data = request.text
    bs = BeautifulSoup(html_data, 'html.parser')

    for tag in bs.find_all('div', class_='ListVerticalImage-items-item'):  # ListVerticalImage-items-item
        name, room, page_url = call_each((process_full_name, process_room, process_page_url), tag)
        yield OldProfessor(str(name), room, pic_url=page_url)


# def create_professors(iterator: iter):
#     out = list()
#     for item in iterator:
#         out.append(OldProfessor(item))


def tag_iterator(url, processor):
    with requests.get(url) as request:
        html_data = request.text
    bs = BeautifulSoup(html_data, 'html.parser')

    for tag in bs.find_all('div', class_='ListVerticalImage-items-item'):
        yield processor(tag)


def tag_iterator2(url, funcs: iter):
    with requests.get(url) as request:
        html_data = request.text
    bs = BeautifulSoup(html_data, 'html.parser')
    for tag in bs.find_all('div', class_='ListVerticalImage-items-item'):
        yield call_each(funcs, tag)


def tag_iterator3(url=RELED_DIR_URL):
    with requests.get(url) as request:
        html_data = request.text
    bs = BeautifulSoup(html_data, 'html.parser')
    for tag in bs.find_all('div', class_='ListVerticalImage-items-item'):
        yield tag


def tag_iterator4(url=RELED_DIR_URL, *args, **kwargs):
    if not args:
        # nonlocal args
        args = 'div',
    if not kwargs:
        # nonlocal kwargs
        kwargs = {'class_': 'ListVerticalImage-items-item'}

    with requests.get(url) as request:
        html_data = request.text
    bs = BeautifulSoup(html_data, 'html.parser')
    for tag in bs.find_all(*args, **kwargs):
        yield tag


professor_iterator = partial(tag_iterator, processor=create_professor)

# def professor_iterator(url=RELED_DIR_URL, processor=None):
#     with requests.get(url) as request:
#         html_data = request.text
#     bs = BeautifulSoup(html_data, 'html.parser')
#
#     if processor is None:
#         processor = create_professor
#
#     for tag in bs.find_all('div', class_='PromoVerticalImage-content'):
#         yield processor(tag)

# class KnowYourProfessorBuilder (FlashcardPowerPoint):
#     def __init__(self):
#         super().__init__()
