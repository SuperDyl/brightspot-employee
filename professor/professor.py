"""
Processes and stores data about Professors in BYU's Religious Education

Classes:
Professor - Store data for a professor in BYU's Religious Education.
ProfessorProcessor - Functions used to get Brightspot employee data.

Constants:
RELIGION_DIR_URL - url for Religious Education at BYU
ProfessorAttributes - Expected fields in a named tuple for a Professor instance
AlternateProfessorAttributes - Alternate expected fields in a named tuple for a Professor instance

"""

from .room import Room
from .tools import remove_prefix, tag_iterator, split_name

from pandas import DataFrame, read_csv
from bs4.element import Tag as BeautifulSoup_Tag

from contextlib import suppress
from typing import Iterable, List, Union, NamedTuple
from os import PathLike

RELIGION_DIR_URL = 'https://religion.byu.edu/directory'


class ProfessorAttributes(NamedTuple):
    first_name: str
    last_name: str
    room: Union[Room, str]
    page_url: str
    telephone: str
    department: str
    job_title: str


class AlternateProfessorAttributes(NamedTuple):
    full_name: str
    room: Union[Room, str]
    page_url: str
    telephone: str
    department: str
    job_title: str


class ProfessorProcessor:
    """
    Functions used to get Brightspot employee data.

    This class assumes html data comes from RELIGION_DIR_URL
    Subclass for use with Professor by setting Professor.processor to a subclass of ProfessorProcessor
    or the processor attribute of a sublass of Professor

    Constants:
    NAME_SUFFIXES - name suffixes (such as jr.) for splitting first/last names
    NON_EXISTENT - value returned for most fields that blank

    """

    NAME_SUFFIXES = ['jr.', 'iii', 'sr.']
    NON_EXISTENT = ''

    @staticmethod
    def process_job_title(tag: BeautifulSoup_Tag) -> str:
        """Return the first job title found in tag"""
        job_title = tag.find(class_='PromoVerticalImage-jobTitle')
        if job_title is None:
            return ProfessorProcessor.NON_EXISTENT
        return job_title.text

    @staticmethod
    def process_department(tag: BeautifulSoup_Tag) -> str:
        """Return the first department found in tag"""
        department = tag.find(class_='PromoVerticalImage-groups')
        if department is None:
            return ProfessorProcessor.NON_EXISTENT
        return department.text

    @staticmethod
    def process_telephone(tag: BeautifulSoup_Tag) -> str:
        """Return the first telephone number found in tag"""
        telephone_tag = tag.find(class_='PromoVerticalImage-phoneNumber')
        if telephone_tag is None:
            return ProfessorProcessor.NON_EXISTENT
        phone_ref = telephone_tag.find('a')['href']
        return remove_prefix(phone_ref, 'tel:')

    @staticmethod
    def process_page_url(tag: BeautifulSoup_Tag) -> str:
        """Return the first hyperlinked url found in tag"""
        return tag.find(class_="Link")['href']

    @staticmethod
    def process_room(tag: BeautifulSoup_Tag) -> Room:
        """Return the first room number found in tag"""
        with suppress(AttributeError):
            room_text = tag.find('p').text.strip()
            return Room.from_string(room_text)
        return Room('', '', '')

    @staticmethod
    def process_first_name(tag: BeautifulSoup_Tag) -> str:
        """Return an estimation of the first name from tag"""
        first_name, _ = ProfessorProcessor.process_split_name(tag)
        return first_name

    @staticmethod
    def process_last_name(tag: BeautifulSoup_Tag) -> str:
        """Return an estimation of the last name from tag"""
        _, last_name = ProfessorProcessor.process_split_name(tag)
        return last_name

    @staticmethod
    def process_full_name(tag: BeautifulSoup_Tag) -> str:
        """Return the first employee name found in tag"""
        return tag.find('a', attrs={'data-cms-ai': '0'})['aria-label'].replace(u'\xa0', u' ')

    @staticmethod
    def process_split_name(tag: BeautifulSoup_Tag) -> (str, str):
        """Return the estimated first and last names from the first employee name found in tag"""
        full_name = ProfessorProcessor.process_full_name(tag)
        return split_name(full_name, ProfessorProcessor.NAME_SUFFIXES)


class Professor:
    """
    Store data for a professor in BYU's Religious Education.

    Class Attributes:
    processor - class used for processing all professor fields
    """

    processor = ProfessorProcessor

    def __init__(self, first_name: str, last_name: str, room_address: Room,
                 page_url: str, telephone: str, department: str, job_title: str):
        self.first_name = first_name
        self.last_name = last_name
        self.room = room_address
        self.page_url = page_url
        self.telephone = telephone
        self.department = department
        self.job_title = job_title

    def __str__(self) -> str:
        return str(self.__dict__)

    def __repr__(self) -> str:
        return str(self)

    def download_photo(self, file_path: PathLike) -> None:
        pass

    @property
    def full_name(self) -> str:
        return ' '.join((self.first_name, self.last_name))

    @full_name.setter
    def full_name(self, new_full_name):
        self.first_name, self.last_name = split_name(new_full_name, name_suffixes=self.processor.NAME_SUFFIXES)

    @classmethod
    def from_html_tag(cls, tag: BeautifulSoup_Tag) -> 'Professor':
        """
        Create a Professor using a BeautifulSoup tag object.

        :param tag: : BeautifulSoup_Tag containing exactly one professor's data
        :return: Professor instance
        """
        first_name, last_name = cls.processor.process_split_name(tag)
        return cls(first_name,
                   last_name,
                   cls.processor.process_room(tag),
                   cls.processor.process_page_url(tag),
                   cls.processor.process_telephone(tag),
                   cls.processor.process_department(tag),
                   cls.processor.process_job_title(tag))

    @classmethod
    def from_named_tuple(cls, kwargs: Union[ProfessorAttributes, AlternateProfessorAttributes]) -> 'Professor':
        """
        Create a Professor using a NamedTuple.

        :param kwargs: : data to fill a new Professor instance
        :return: Professor instance
        """
        room_address = kwargs.room if isinstance(kwargs.room, Room) else Room.from_string(kwargs.room)
        if not ('first_name' in kwargs._fields and 'last_name' in kwargs._fields):
            first_name, last_name = split_name(kwargs.full_name, cls.processor.NAME_SUFFIXES)
        else:
            first_name, last_name = kwargs.first_name, kwargs.last_name
        return cls(first_name,
                   last_name,
                   room_address,
                   kwargs.page_url,
                   kwargs.telephone,
                   kwargs.department,
                   kwargs.job_title)

    @staticmethod
    def to_csv(file_path: PathLike, professors: Iterable['Professor']) -> None:
        """
        Create a comma-seperated-values file at file_path.

        :param file_path: : path to save the csv file to
        :param professors: Professor objects to be included in the file
        """
        dataframe = DataFrame.from_records((p.__dict__ for p in professors))
        dataframe.to_csv(file_path)

    @staticmethod
    def from_csv(file_path: PathLike) -> List['Professor']:
        """
        Create a list of Professor instances from a proper csv file.
        The csv file must contain every header/column that Professor uses for its attributes

        :param file_path: : path to load the csv file from
        :return: list of Professor instances from the file's data
        """
        dataframe = read_csv(file_path, keep_default_na=False)
        return [Professor.from_named_tuple(row) for row in dataframe.itertuples()]

    @staticmethod
    def from_website(url: str = RELIGION_DIR_URL) -> List['Professor']:
        """
        Return a list of Professor instances using data from the website at url.
        The url is only guaranteed to work at RELIGION_DIR_URL, the default url

        :param url: : webpage to pull all data from
        :return: list of Professor instances from the url's data
        """
        return [Professor.from_html_tag(tag) for tag in tag_iterator(url)]
