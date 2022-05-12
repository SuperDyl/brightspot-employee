"""
Processes and stores data about Employees on BrightSpot pages.

Classes:
Employee - Store data for an employee.
EmployeeProcessor - Functions used to get BrightSpot employee data.

Constants:
EmployeeAttributes - Expected fields in a named tuple for an Employee instance
AlternateEmployeeAttributes - Alternate expected fields in a named tuple for an Employee instance

"""

from .room import Room
from . import util

from pandas import DataFrame, read_csv
from bs4.element import Tag as BeautifulSoup_Tag
import requests

from contextlib import suppress
from typing import Iterable, List, Union, Optional, NamedTuple, TypeVar, Type
from os import path, makedirs, PathLike
from pathlib import Path


class EmployeeAttributes(NamedTuple):
    first_name: str
    last_name: str
    room: Union[Room, str]
    page_url: str
    telephone: str
    department: str
    job_title: str


class AlternateEmployeeAttributes(NamedTuple):
    full_name: str
    room: Union[Room, str]
    page_url: str
    telephone: str
    department: str
    job_title: str


class EmployeeProcessor:
    """
    Functions used to get BrightSpot employee data.

    Subclass for use with Employee by setting Employee.processor to a subclass of EmployeeProcessor
    or the processor attribute of a subclass of Employee

    Constants:
    NAME_SUFFIXES - name suffixes (such as jr.) for splitting first/last names.
    NON_EXISTENT - value returned for most fields that blank.

    """

    NAME_SUFFIXES = util.NAME_SUFFIXES[:]
    NON_EXISTENT = ''

    def __init__(self, container: str):
        self.container = container

    def process_job_title(self, tag: BeautifulSoup_Tag) -> str:
        """Return the first job title found in tag."""
        job_title = tag.find(class_=(self.container + '-jobTitle'))
        if job_title is None:
            return self.NON_EXISTENT
        return job_title.text

    def process_department(self, tag: BeautifulSoup_Tag) -> str:
        """Return the first department found in tag."""
        department = tag.find(class_=(self.container + '-groups'))
        if department is None:
            return self.NON_EXISTENT
        return department.text

    def process_telephone(self, tag: BeautifulSoup_Tag) -> str:
        """Return the first telephone number found in tag."""
        telephone_tag = tag.find(class_=(self.container + '-phoneNumber'))
        if telephone_tag is None:
            return self.NON_EXISTENT
        phone_ref = telephone_tag.find('a')['href']
        return util.remove_prefix(phone_ref, 'tel:')

    @staticmethod
    def process_page_url_static(tag: BeautifulSoup_Tag) -> str:
        """Return the first hyperlinked url found in tag, but static."""
        return tag.find(class_="Link")['href']

    def process_page_url(self, tag: BeautifulSoup_Tag) -> str:
        """Return the first hyperlinked url found in tag."""
        return type(self).process_page_url_static(tag)

    @staticmethod
    def process_room_static(tag: BeautifulSoup_Tag) -> Room:
        """Return the first room number found in tag, but static"""
        with suppress(AttributeError):
            room_text = tag.find('p').text.strip()
            return Room.from_string(room_text)
        return Room('', '', '')

    def process_room(self, tag: BeautifulSoup_Tag) -> Room:
        """Return the first room number found in tag."""
        return type(self).process_room_static(tag)

    def process_first_name(self, tag: BeautifulSoup_Tag) -> str:
        """Return an estimation of the first name from tag"""
        first_name, _ = self.process_split_name(tag)
        return first_name

    def process_last_name(self, tag: BeautifulSoup_Tag) -> str:
        """Return an estimation of the last name from tag"""
        _, last_name = self.process_split_name(tag)
        return last_name

    @staticmethod
    def process_full_name_static(tag: BeautifulSoup_Tag) -> str:
        """Return the first employee name found in tag, but static."""
        return tag.find('a', attrs={'data-cms-ai': '0'})['aria-label'].replace(u'\xa0', u' ')

    def process_full_name(self, tag: BeautifulSoup_Tag) -> str:
        """Return the first employee name found in tag."""
        return type(self).process_full_name_static(tag)

    def process_split_name(self, tag: BeautifulSoup_Tag) -> (str, str):
        """Return the estimated first and last names from the first employee name found in tag"""
        full_name = self.process_full_name(tag)
        return util.split_name(full_name, self.NAME_SUFFIXES)


E = TypeVar('E', bound='Employee')


class Employee:
    """
    Store data for a BrightSpot employee.
    Employee.processor must be set depending on the website being scraped from

    Class Attributes:
    processor - class used for processing all employee fields
    """

    processor = EmployeeProcessor('')

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

    def download_photo(self, dir_path: Union[PathLike, str], file_name: Optional[str] = None) -> None:
        """
        Download full-resolution photo from page_url.

        :param dir_path: : location to store the image
        :param file_name: : name to give the image. If blank, will be saved as full_name.[jpg/png]
        :return: None
        """
        tag = util.tag_iterator(self.page_url, args=('meta',), kwargs={'property': 'og:image:url'})
        image_url = tag[0]['content']
        img_request = requests.get(image_url)

        if file_name is None:
            file_extension_buffer = 10
            file_name = self.full_name + Path(image_url[-file_extension_buffer:]).suffix

        dir_path = Path(dir_path)
        makedirs(dir_path, exist_ok=True)
        with open(path.join(dir_path, file_name), 'wb') as file:
            for chunk in img_request.iter_content():
                file.write(chunk)

    @property
    def full_name(self) -> str:
        return ' '.join((self.first_name, self.last_name))

    @full_name.setter
    def full_name(self, new_full_name):
        self.first_name, self.last_name = util.split_name(new_full_name, name_suffixes=self.processor.NAME_SUFFIXES)

    @classmethod
    def from_html_tag(cls: Type[E], tag: BeautifulSoup_Tag) -> Type[E]:
        """
        Create an Employee using a BeautifulSoup tag object.

        :param tag: : BeautifulSoup_Tag containing exactly one employee's data
        :return: Employee instance
        """
        first_name, last_name = cls.processor.process_split_name(tag)
        return cls(first_name,
                   last_name,
                   cls.processor.process_room(tag),
                   cls.processor.process_page_url(tag),
                   cls.processor.process_telephone(tag),
                   cls.processor.process_department(tag),
                   cls.processor.process_job_title(tag)
                   )

    @classmethod
    def from_named_tuple(cls: Type[E], kwargs: Union[EmployeeAttributes, AlternateEmployeeAttributes]) -> Type[E]:
        """
        Create an Employee using a NamedTuple.

        :param kwargs: : data to fill a new Employee instance
        :return: Employee instance
        """
        room_address = kwargs.room if isinstance(kwargs.room, Room) else Room.from_string(kwargs.room)
        if not ('first_name' in kwargs._fields and 'last_name' in kwargs._fields):
            first_name, last_name = util.split_name(kwargs.full_name, cls.processor.NAME_SUFFIXES)
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
    def to_csv(file_path: Union[PathLike, str], employees: Iterable[Type[E]]) -> None:
        """
        Create a comma-seperated-values file at file_path.

        :param file_path: : path to save the csv file to
        :param employees: Employee objects to be included in the file
        """
        dataframe = DataFrame.from_records((
                                            {k: v
                                                for k, v in p.__dict__.items()
                                                if k in EmployeeAttributes._fields}
                                            for p in employees))
        dataframe.to_csv(Path(file_path))

    @staticmethod
    def from_csv(file_path: Union[PathLike, str]) -> List[Type[E]]:
        """
        Create a list of Employee instances from a proper csv file.
        The csv file must contain every header/column that Employee uses for its attributes

        :param file_path: : path to load the csv file from
        :return: list of Employee instances from the file's data
        """
        dataframe = read_csv(Path(file_path), keep_default_na=False)
        return [Employee.from_named_tuple(row) for row in dataframe.itertuples()]

    @classmethod
    def from_website(cls: Type[E], url: str) -> List[Type[E]]:
        """
        Return a list of Employee instances using data from the website at url.
        The url is only guaranteed to work at RELIGION_DIR_URL, the default url

        :param url: : webpage to pull all data from
        :return: list of Employee instances from the url's data
        """
        return [cls.from_html_tag(tag) for tag in util.tag_iterator(url)]

    @staticmethod
    def download_all_photos(professors: Iterable['Employee'], dir_path: PathLike,
                            thread_limit: int = 5) -> None:
        """
        Download each employee's photo and save it in dir_path using the default naming
        Uses multithreading
        Default naming uses Employee.full_name and the original file extension

        :param professors: : all employees to download photos for. Each must have a page_url
        :param dir_path: directory to store all the photos in
        :param thread_limit: number of photos to download simultaneously
        """
        functions = (prof.download_photo for prof in professors)
        util.stepped_limited_multithread(functions, args=(dir_path,), limit=thread_limit)
