# from flashcard_powerpoint import FlashcardPowerPoint
from professor import Professor
from room import Room

from bs4 import BeautifulSoup
import requests

# import re
from functools import partial

RELED_DIR_URL = 'https://religion.byu.edu/directory'
NAME_SUFFIXES = ('jr.', 'iii', 'sr.')


def remove_prefix(string: str, pref: str):
    if pref == string[0:len(pref)]:
        return string[len(pref):-1]
    return string


def call_each(funcs: iter, *args, **kwargs):
    return (x(*args, **kwargs) for x in funcs)


def process_room(tag):
    try:
        room = tag.find('p').text.strip()
        room = Room.from_string(room)
    except (IndexError, AttributeError):
        return Room('', '', '')
    except TypeError:
        print("I'll fix this later")
        return Room('', '', '')
    return room


def process_first_name(tag):
    first_name, _ = process_split_name(tag)
    return first_name


def process_last_name(tag):
    _, last_name = process_split_name(tag)
    return last_name


def process_split_name(tag) -> (str, str):
    full_name = process_full_name(tag)
    full_split_name = full_name.split(' ')
    if full_split_name[-1].lower() in NAME_SUFFIXES:
        *first, last = full_split_name[:-1]
        return ' '.join(first), ' '.join((last, full_split_name[-1]))
    # else
    *first, last = full_split_name
    return ' '.join(first), last


def process_full_name(tag):
    return tag.find('a', attrs={'data-cms-ai': '0'})['aria-label'].replace(u'\xa0', u' ')


def process_page_url(tag):
    return tag.find(class_="Link").href


def process_telephone(tag):
    out = tag.find_all(class_='PromoVerticalImage-phoneNumber')
    if not out:
        return ''
    out = out[0].find('a')['href']
    out = remove_prefix(out, 'tel:')
    return out


def process_department(tag):
    out = tag.find_all(class_='PromoVerticalImage-groups')
    if not out:
        return ''
    return out[0].string


def process_job_title(tag):
    out = tag.find(class_='PromoVerticalImage-jobTitle')
    if out is None:
        return ''
    return out.text


def create_professor(tag):
    name, room, page_url = call_each((process_full_name, process_room, process_page_url), tag)
    return Professor(str(name), room, pic_url=page_url)


def create_professor2(url=RELED_DIR_URL):
    with requests.get(url) as request:
        html_data = request.text
    bs = BeautifulSoup(html_data, 'html.parser')

    for tag in bs.find_all('div', class_='ListVerticalImage-items-item'):  # ListVerticalImage-items-item
        name, room, page_url = call_each((process_full_name, process_room, process_page_url), tag)
        yield Professor(str(name), room, pic_url=page_url)


def create_professors(iterator: iter):
    out = list()
    for item in iterator:
        out.append(Professor(item))


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
