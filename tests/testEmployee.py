from src.professor import Employee, EmployeeProcessor

from tempfile import NamedTemporaryFile, TemporaryDirectory
import unittest


RELIGION_DIR_URL = 'https://religion.byu.edu/directory'


class TestProfessor(unittest.TestCase):
    def setUp(self) -> None:
        Employee.processor = EmployeeProcessor('PromoVerticalImage')
        self.all_profs = Employee.from_website(RELIGION_DIR_URL)

    def test_csv(self):
        all_profs = self.all_profs

        with NamedTemporaryFile('w+') as file:
            a = '\n'.join(tuple(str(x) for x in all_profs))
            Employee.to_csv(file.name, all_profs)

            csv = Employee.from_csv(file.name)
            b = '\n'.join(tuple(str(x) for x in csv))
        self.assertEqual(a, b)

    def test_download_photo(self):
        with TemporaryDirectory() as temp_dir:
            self.all_profs[0].download_photo(temp_dir)


if __name__ == '__main__':
    unittest.main()
