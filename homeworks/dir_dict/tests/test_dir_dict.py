import pathlib
import time
from unittest import TestCase

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

        # не всегда удаляет сразу, даём ОС время всё почистить
        time.sleep(0.5)
        self.assertEqual(False, self.p.exists())

    def test_create_dict(self):
        self.d['lang'] = 'Python\n'
        p1 = pathlib.Path(self.test_path) / 'lang'
        self.assertTrue(self.p.exists())
        self.assertTrue(self.p.is_dir())
        self.assertTrue(p1.exists())
        self.assertFalse(p1.is_dir())

    def test_use_dict(self):
        self.d['lang'] = 'Python\n'
        self.assertEqual('Python\n', self.d['lang'])

        self.d.setdefault('name')
        self.assertEqual('None', self.d['name'])

        self.assertEqual('Python\n', self.d.get('lang'))

        pop_key = self.d.pop('lang')
        self.assertEqual('Python\n', pop_key)
        with self.assertRaises(KeyError):
            self.d['lang']

        self.assertEqual('None', self.d.get('lang'))