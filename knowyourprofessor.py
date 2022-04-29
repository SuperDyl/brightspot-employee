# from flashcard_powerpoint import FlashcardPowerPoint
# import tools
# from oldprofessor import OldProfessor
import professor
# from tools import call_each  # ,  # remove_prefix
# from room import RoomOld
#
# from bs4 import BeautifulSoup
# import requests

# import re
# from functools import partial


RELED_DIR_URL = professor.RELIGION_DIR_URL
NAME_SUFFIXES = professor.ProfessorProcessor.NAME_SUFFIXES


# def create_professor(tag):
#     name, room, page_url = call_each((process_full_name, process_room, process_page_url), tag)
#     return OldProfessor(str(name), room, pic_url=page_url)
#
#
# def create_professor2(url=RELED_DIR_URL):
#     with requests.get(url) as request:
#         html_data = request.text
#     bs = BeautifulSoup(html_data, 'html.parser')
#
#     for tag in bs.find_all('div', class_='ListVerticalImage-items-item'):  # ListVerticalImage-items-item
#         name, room, page_url = call_each((process_full_name, process_room, process_page_url), tag)
#         yield OldProfessor(str(name), room, pic_url=page_url)


# def create_professors(iterator: iter):
#     out = list()
#     for item in iterator:
#         out.append(OldProfessor(item))


# def tag_iterator(url, processor):
#     with requests.get(url) as request:
#         html_data = request.text
#     bs = BeautifulSoup(html_data, 'html.parser')
#
#     for tag in bs.find_all('div', class_='ListVerticalImage-items-item'):
#         yield processor(tag)


# professor_iterator = partial(tag_iterator, processor=create_professor)

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
