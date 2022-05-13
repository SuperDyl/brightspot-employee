from src.brightspot_employee import Employee, EmployeeProcessor

from bs4.element import Tag as BeautifulSoup_Tag

from tempfile import NamedTemporaryFile, TemporaryDirectory
import unittest
from typing import Optional


RELIGION_DIR_URL = 'https://religion.byu.edu/directory'


class TestProfessor(unittest.TestCase):
    def setUp(self) -> None:
        Employee.processor = EmployeeProcessor('PromoVerticalImage', 'ListVerticalImage-items')
        self.all_religion_employees = Employee.from_website(RELIGION_DIR_URL)

    def test_csv(self):
        with NamedTemporaryFile('w+') as file:
            a = '\n'.join(tuple(str(x) for x in self.all_religion_employees))
            Employee.to_csv(file.name, self.all_religion_employees)

            csv = Employee.from_csv(file.name)
            b = '\n'.join(tuple(str(x) for x in csv))
        self.assertEqual(a, b)

    def test_download_photo(self):
        with TemporaryDirectory() as temp_dir:
            self.all_religion_employees[0].download_photo(temp_dir)

    def test_byu_humanities_website(self):
        employees = Employee.from_website('https://hum.byu.edu/directory')
        self.assertGreater(len(employees), 0)

    def test_byu_cs_website(self):
        class CompSciProcessor(EmployeeProcessor):
            NAME_SEARCH_TEXT = '-title'

            def __init__(self, container: str = 'card', super_container: Optional[str] = None):
                super().__init__(container, super_container)

            def process_job_title(self, tag: BeautifulSoup_Tag, search_text: str = 'subtitle') -> str:
                return super().process_job_title(tag, search_text)

            def process_full_name(self, tag: BeautifulSoup_Tag, search_text: Optional[str] = NAME_SEARCH_TEXT) -> str:
                if search_text is None:
                    search_text = self.NAME_SEARCH_TEXT
                return tag.find('div', class_=(self.container + search_text)).text.replace(u'\xa0', u' ')

            def process_page_url(self, tag: BeautifulSoup_Tag, search_text: str = 'btn accent') -> str:
                return super().process_page_url(tag, search_text)

        class CompSciEmployee(Employee):
            processor = CompSciProcessor()

        urls = [r'https://cs.byu.edu/department/directory/faculty-directory/',
                r'https://cs.byu.edu/department/directory/staff-directory/',
                r'https://cs.byu.edu/department/directory/systems-and-network-adminstrators/',
                r'https://cs.byu.edu/department/directory/part-time-faculty-directory/',
                r'https://cs.byu.edu/department/directory/emeritus-faculty-directory/'
                ]

        for index, url in enumerate(urls):
            employees = CompSciEmployee.from_website(url)
            with self.subTest(msg=f'Testing: {urls[index]}', i=index):
                self.assertGreater(len(employees), 0)

    def test_byu_history(self):
        class HistoryEmployee(Employee):
            processor = EmployeeProcessor('PromoIconOnTopLarge', 'List-items-item')

        employees = HistoryEmployee.from_website('https://history.byu.edu/directories?')
        self.assertGreater(len(employees), 0)


if __name__ == '__main__':
    unittest.main()
