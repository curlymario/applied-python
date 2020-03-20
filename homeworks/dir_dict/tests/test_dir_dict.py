from unittest import TestCase
import pathlib

from dir_dict import DirDict


class DirDictTestCase(TestCase):

    test_path = '/tmp/dirdict'

    def setUp(self):
        self.d = DirDict(self.test_path)
        self.p = pathlib.Path(self.test_path)

    def tearDown(self):
        for file in self.p.iterdir():
            file.unlink()
        self.p.rmdir()
        self.assertEqual(False, self.p.exists())

    def test_create_dict(self):
        self.d['lang'] = 'Python\n'
        p1 = pathlib.Path(self.test_path) / 'lang'
        self.assertEqual(True, self.p.exists())
        self.assertEqual(True, self.p.is_dir())
        self.assertEqual(True, p1.exists())
        self.assertEqual(False, p1.is_dir())
