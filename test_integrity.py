import unittest
import io, sys
from TellStones import Stone, Reserve, Board, TellStones

class StoneTest(unittest.TestCase):
    def setUp(self):
        self.stone_a = Stone("A")
        self.stone_b = Stone("B")
        self.stone_a_hidden = Stone("A", hidden=True)
        self.stone_a_not_hidden = Stone("A", hidden=False)

    def test_default_not_hidden(self):
        self.assertFalse(self.stone_a.hidden)

    def test_equality(self):
        self.assertEqual(self.stone_a, Stone("A"))
        self.assertNotEqual(self.stone_a, self.stone_b)
        self.assertNotEqual(self.stone_a_hidden, self.stone_a_not_hidden)

    def test_flip(self):
        self.stone_a_not_hidden.flip()
        self.assertTrue(self.stone_a_not_hidden.hidden)
        self.stone_a_not_hidden.flip()
        self.assertFalse(self.stone_a_not_hidden.hidden)
    
    def test_repr(self):
        self.assertEqual(repr(self.stone_a_not_hidden), "A")
        self.assertEqual(repr(self.stone_a_hidden), "*")

class ReserveTest(unittest.TestCase):
    def setUp(self):
        self.reserve = Reserve(Stone("A"), Stone("B"))

    def test_remove_stone(self):
        self.reserve.remove_stone("A")
        self.assertNotIn(Stone("A"), self.reserve)

class BoardTest(unittest.TestCase):
    def setUp(self):
        self.board = Board("A", "B")
    
    def test_place(self):
        self.board.place("C")
        self.assertEqual(self.board[-1], Stone("C"))
        self.board.place("D", position="left")
        self.assertEqual(self.board[0], Stone("D"))

    def test_peek(self):
        self.board[0].flip()
        captured_output = io.StringIO() # crea un buffer per catturare l'output
        sys.stdout = captured_output  # reindirizza stdout al buffer
        self.board.peek(1)
        sys.stdout = sys.__stdout__ # ripristina stdout
        self.assertEqual(captured_output.getvalue().strip(), "A") 