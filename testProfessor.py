from professor import Professor, tag_iterator

from tempfile import NamedTemporaryFile
import unittest


RELIGION_DIR_URL = 'https://religion.byu.edu/directory'


class TestProfessor(unittest.TestCase):
    def test_csv(self):
        all_profs = [Professor.from_html_tag(tag) for tag in tag_iterator(RELIGION_DIR_URL)]

        with NamedTemporaryFile('w+') as file:
            a = '\n'.join(tuple(str(x) for x in all_profs))
            Professor.to_csv(file.name, all_profs)

            csv = Professor.from_csv(file.name)
            b = '\n'.join(tuple(str(x) for x in csv))
        self.assertEqual(a, b)


if __name__ == '__main__':
    unittest.main()
