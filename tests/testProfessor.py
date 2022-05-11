from src.professor import Professor

from tempfile import NamedTemporaryFile
import unittest


RELIGION_DIR_URL = 'https://religion.byu.edu/directory'


class TestProfessor(unittest.TestCase):
    def setUp(self) -> None:
        self.all_profs = Professor.from_website()

    def test_csv(self):
        all_profs = self.all_profs

        with NamedTemporaryFile('w+') as file:
            a = '\n'.join(tuple(str(x) for x in all_profs))
            Professor.to_csv(file.name, all_profs)

            csv = Professor.from_csv(file.name)
            b = '\n'.join(tuple(str(x) for x in csv))
        self.assertEqual(a, b)

    def test_download_photo(self):
        self.all_profs[0].download_photo('pics')


if __name__ == '__main__':
    unittest.main()
