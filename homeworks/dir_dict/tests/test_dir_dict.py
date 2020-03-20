from unittest import TestCase
import pathlib

from dir_dict import DirDict


class DirDictTestCase(TestCase):

    def test_text__create(self):
        d = DirDict('/tmp/dirdict')
        d['lang'] = 'Python\n'
        p = pathlib.Path('/tmp/dirdict')
        p1 = pathlib.Path('/tmp/dirdict/lang')

        self.assertEqual(True, p.exists())
        self.assertEqual(True, p.is_dir())
        self.assertEqual(True, p1.exists())
        self.assertEqual(False, p1.is_dir())

        p1.unlink()
        p.rmdir()
        self.assertEqual(False, p.exists())
