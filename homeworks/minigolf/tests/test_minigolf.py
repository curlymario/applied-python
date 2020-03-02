from unittest import TestCase

from minigolf import HitsMatch, HolesMatch, Player


class HitsMatchTestCase(TestCase):
    def setUp(self):
        self.players = [Player('A'), Player('B'), Player('C')]
        self.m = HitsMatch(3, self.players)

    def tearDown(self):
        self.players = None
        self.m = None

    def _first_hole_hits(self):
        self.m.hit()  # 1
        self.m.hit()  # 2
        self.m.hit(True)  # 3
        self.m.hit(True)  # 1
        for _ in range(8):
            self.m.hit()  # 2

    def _second_hole_hits(self):
        self.m.hit()  # 2
        for _ in range(3):
            self.m.hit(True)  # 3, 1, 2

    def _third_hole_hits_one(self):
        self.m.hit()  # 3
        self.m.hit(True)  # 1
        self.m.hit()  # 2

    def _third_hole_hits_two(self):
        self.m.hit(True)  # 3
        self.m.hit()  # 2
        self.m.hit(True)  # 2

    def test_first_hole__not_finished(self):
        self._first_hole_hits()
        self.assertFalse(self.m.finished)

    def test_first_hole__get_table(self):
        self._first_hole_hits()
        self.assertEqual(self.m.get_table(), [
            ('A', 'B', 'C'),
            (2, 10, 1),
            (None, None, None),
            (None, None, None),
        ])

    def test_second_hole__not_finished(self):
        self._first_hole_hits()
        self._second_hole_hits()
        self.assertFalse(self.m.finished)

    def test_second_hole__get_table(self):
        self._first_hole_hits()
        self._second_hole_hits()
        self.assertEqual(self.m.get_table(), [
            ('A', 'B', 'C'),
            (2, 10, 1),
            (1, 2, 1),
            (None, None, None),
        ])

    def test_second_hole__no_winners(self):
        self._first_hole_hits()
        self._second_hole_hits()
        with self.assertRaises(RuntimeError):
            self.m.get_winners()

    def test_third_hole__get_table(self):
        self._first_hole_hits()
        self._second_hole_hits()
        self._third_hole_hits_one()
        self.assertEqual(self.m.get_table(), [
            ('A', 'B', 'C'),
            (2, 10, 1),
            (1, 2, 1),
            (1, None, None),
        ])

    def test_third_hole__finished(self):
        self._first_hole_hits()
        self._second_hole_hits()
        self._third_hole_hits_one()
        self._third_hole_hits_two()
        self.assertTrue(self.m.finished)

    def test_third_hole__get_table_last(self):
        self._first_hole_hits()
        self._second_hole_hits()
        self._third_hole_hits_one()
        self._third_hole_hits_two()
        self.assertEqual(self.m.get_table(), [
            ('A', 'B', 'C'),
            (2, 10, 1),
            (1, 2, 1),
            (1, 3, 2),
        ])

    def test_no_more_hits(self):
        self._first_hole_hits()
        self._second_hole_hits()
        self._third_hole_hits_one()
        self._third_hole_hits_two()
        with self.assertRaises(RuntimeError):
            self.m.hit()

    def test_final_winners(self):
        self._first_hole_hits()
        self._second_hole_hits()
        self._third_hole_hits_one()
        self._third_hole_hits_two()
        self.assertEqual(self.m.get_winners(), [
            self.players[0], self.players[2]
        ])


class HolesMatchTestCase(TestCase):
    def setUp(self):
        self.players = [Player('A'), Player('B'), Player('C')]
        self.m = HolesMatch(3, self.players)

    def tearDown(self):
        self.players = None
        self.m = None

    def _first_hole(self):
        self.m.hit(True) # 1
        self.m.hit()     # 2
        self.m.hit()     # 3

    def _second_hole(self):
        for _ in range(10):
            for _ in range(3):
                self.m.hit() # 2, 3, 1

    def _third_hole_one(self):
        for _ in range(9):
            for _ in range(3):
                self.m.hit() # 3, 1, 2
        self.m.hit(True) # 3

    def _third_hole_two(self):
        self.m.hit(True) # 1
        self.m.hit()     # 2

    def test_first_hole_table(self):
        self._first_hole()
        self.assertFalse(self.m.finished)
        self.assertEqual(self.m.get_table(), [
            ('A', 'B', 'C'),
            (1, 0, 0),
            (None, None, None),
            (None, None, None),
        ])

    def test_second_hole_table(self):
        self._first_hole()
        self._second_hole()
        self.assertFalse(self.m.finished)
        self.assertEqual(self.m.get_table(), [
            ('A', 'B', 'C'),
            (1, 0, 0),
            (0, 0, 0),
            (None, None, None),
        ])

    def test_second_hole_winners(self):
        self._first_hole()
        self._second_hole()
        with self.assertRaises(RuntimeError):
            self.m.get_winners()

    def test_third_hole_one_table(self):
        self._first_hole()
        self._second_hole()
        self._third_hole_one()
        self.assertEqual(self.m.get_table(), [
            ('A', 'B', 'C'),
            (1, 0, 0),
            (0, 0, 0),
            (None, None, 1),
        ])

    def test_third_hole_two_table(self):
        self._first_hole()
        self._second_hole()
        self._third_hole_one()
        self._third_hole_two()
        self.assertTrue(self.m.finished)
        self.assertEqual(self.m.get_table(), [
            ('A', 'B', 'C'),
            (1, 0, 0),
            (0, 0, 0),
            (1, 0, 1),
        ])

    def test_third_hole_winners(self):
        self._first_hole()
        self._second_hole()
        self._third_hole_one()
        self._third_hole_two()
        with self.assertRaises(RuntimeError):
            self.m.hit()

        self.assertEqual(self.m.get_winners(), [self.players[0]])




