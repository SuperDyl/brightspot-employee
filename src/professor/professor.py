"""
Processes and stores data about Professors in BYU's Religious Education

Classes:
Professor - Store data for a professor in BYU's Religious Education.
ProfessorProcessor - Functions used to get BrightSpot employee data.

Constants:
RELIGION_DIR_URL - url for Religious Education at BYU
ProfessorAttributes - Expected fields in a named tuple for a Professor instance
AlternateProfessorAttributes - Alternate expected fields in a named tuple for a Professor instance

"""

from .employee import *

from .room import Room
from . import util

from pandas import DataFrame, read_csv
from bs4.element import Tag as BeautifulSoup_Tag
import requests

from contextlib import suppress
from typing import Iterable, List, Union, Optional, NamedTuple
from os import path, makedirs, PathLike
from pathlib import Path

RELIGION_DIR_URL = 'https://religion.byu.edu/directory'

ProfessorAttributes = EmployeeAttributes
AlternateProfessorAttributes = AlternateEmployeeAttributes


class ProfessorProcessor(EmployeeProcessor):
    """
    Functions used to get employee data for Religious Education faculty and staff.

    This class assumes html data comes from RELIGION_DIR_URL
    Subclass for use with Professor by setting Professor.processor to a subclass of ProfessorProcessor
    or the processor attribute of a subclass of Professor

    Constants:
    NAME_SUFFIXES - name suffixes (such as jr.) for splitting first/last names
    NON_EXISTENT - value returned for most fields that blank

    """

    DEFAULT_CONTAINER = 'PromoVerticalImage'

    @staticmethod
    def process_job_title(tag: BeautifulSoup_Tag, container: str = DEFAULT_CONTAINER) -> str:
        """Return the first job title found in tag"""
        return EmployeeProcessor.process_job_title(tag, container)

    @staticmethod
    def process_department(tag: BeautifulSoup_Tag, container: str = DEFAULT_CONTAINER) -> str:
        """Return the first department found in tag"""
        return EmployeeProcessor.process_department(tag, container)

    @staticmethod
    def process_telephone(tag: BeautifulSoup_Tag, container: str = DEFAULT_CONTAINER) -> str:
        """Return the first telephone number found in tag"""
        return EmployeeProcessor.process_telephone(tag, container)

    process_page_url = EmployeeProcessor.process_page_url

    process_room = EmployeeProcessor.process_room

    process_first_name = EmployeeProcessor.process_first_name

    process_last_name = EmployeeProcessor.process_last_name

    process_full_name = EmployeeProcessor.process_full_name

    process_split_name = EmployeeProcessor.process_split_name


class Professor(Employee):
    """
    Store data for a professor in BYU's Religious Education.

    Class Attributes:
    processor - class used for processing all professor fields
    """

    processor = ProfessorProcessor

    def __init__(self, first_name: str, last_name: str, room_address: Room,
                 page_url: str, telephone: str, department: str, job_title: str):
        super().__init__(first_name, last_name, room_address, page_url, telephone, department, job_title)

    # def __str__(self) -> str:
    #     return super().__str__()
    #
    # def __repr__(self) -> str:
    #     return str(self)
    #
    # def download_photo(self, dir_path: path, file_name: Optional[str] = None) -> None:
    #     """
    #     Download full-resolution photo from page_url.
    #
    #     :param dir_path: : location to store the image
    #     :param file_name: : name to give the image. If blank, will be saved as full_name.[jpg/png]
    #     :return: None
    #     """
    #     tag = util.tag_iterator(self.page_url, args=('meta',), kwargs={'property': 'og:image:url'})
    #     image_url = tag[0]['content']
    #     img_request = requests.get(image_url)
    #
    #     if file_name is None:
    #         file_extension_buffer = 10
    #         file_name = self.full_name + Path(image_url[-file_extension_buffer:]).suffix
    #
    #     dir_path = Path(dir_path)
    #     makedirs(dir_path, exist_ok=True)
    #     with open(path.join(dir_path, file_name), 'wb') as file:
    #         for chunk in img_request.iter_content():
    #             file.write(chunk)
    #
    # @property
    # def full_name(self) -> str:
    #     return ' '.join((self.first_name, self.last_name))
    #
    # @full_name.setter
    # def full_name(self, new_full_name):
    #     self.first_name, self.last_name = util.split_name(new_full_name, name_suffixes=self.processor.NAME_SUFFIXES)

    @classmethod
    def from_html_tag(cls, tag: BeautifulSoup_Tag, container: str = ProfessorProcessor.DEFAULT_CONTAINER)\
            -> 'Professor':  # TODO: fix return type
        """
        Create a Professor using a BeautifulSoup tag object.

        :param tag: : BeautifulSoup_Tag containing exactly one professor's data
        :param container: : name of container used to separate employees on BrightSpot page
        :return: Professor instance
        """
        return Employee.from_html_tag(tag, container)

    # @classmethod
    # def from_named_tuple(cls, kwargs: Union[ProfessorAttributes, AlternateProfessorAttributes]) -> 'Employee':
    #     """
    #     Create a Employee using a NamedTuple.
    #
    #     :param kwargs: : data to fill a new Employee instance
    #     :return: Employee instance
    #     """
    #     room_address = kwargs.room if isinstance(kwargs.room, Room) else Room.from_string(kwargs.room)
    #     if not ('first_name' in kwargs._fields and 'last_name' in kwargs._fields):
    #         first_name, last_name = util.split_name(kwargs.full_name, cls.processor.NAME_SUFFIXES)
    #     else:
    #         first_name, last_name = kwargs.first_name, kwargs.last_name
    #     return cls(first_name,
    #                last_name,
    #                room_address,
    #                kwargs.page_url,
    #                kwargs.telephone,
    #                kwargs.department,
    #                kwargs.job_title)
    #
    # @staticmethod
    # def to_csv(file_path: PathLike, professors: Iterable['Professor']) -> None:
    #     """
    #     Create a comma-seperated-values file at file_path.
    #
    #     :param file_path: : path to save the csv file to
    #     :param professors: Employee objects to be included in the file
    #     """
    #     dataframe = DataFrame.from_records((p.__dict__ for p in professor))
    #     dataframe.to_csv(Path(file_path))
    #
    # @staticmethod
    # def from_csv(file_path: PathLike) -> List['Professor']:
    #     """
    #     Create a list of Professor instances from a proper csv file.
    #     The csv file must contain every header/column that Employee uses for its attributes
    #
    #     :param file_path: : path to load the csv file from
    #     :return: list of Professor instances from the file's data
    #     """
    #     dataframe = read_csv(Path(file_path), keep_default_na=False)
    #     return [Professor.from_named_tuple(row) for row in dataframe.itertuples()]

    @staticmethod
    def from_website(url: str = RELIGION_DIR_URL, container: str = ProfessorProcessor.DEFAULT_CONTAINER)\
            -> List[Employee]:
        """
        Return a list of Employee instances using data from the website at url.
        The url is only guaranteed to work at RELIGION_DIR_URL, the default url

        :param url: : webpage to pull all data from
        :param container: : name of container used to separate employees on BrightSpot page
        :return: list of Employee instances from the url's data
        """
        return Employee.from_website(url, Professor.processor.DEFAULT_CONTAINER)

    # @staticmethod
    # def download_all_photos(professors: Iterable['Professor'], dir_path: PathLike,
    #                         thread_limit: int = 5) -> None:
    #     """
    #     Download each professor's photo and save it in dir_path using the default naming
    #     Uses multithreading
    #     Default naming uses Professor.full_name and the original file extension
    #
    #     :param professors: : all professors to download photos for. Each must have a page_url
    #     :param dir_path: directory to store all the photos in
    #     :param thread_limit: number of photos to download simultaneously
    #     """
    #     functions = (prof.download_photo for prof in professors)
    #     util.stepped_limited_multithread(functions, args=(dir_path,), limit=thread_limit)
