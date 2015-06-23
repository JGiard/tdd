from unittest import TestCase
from unittest.mock import Mock

from pendu import HangmanComputer, State, OutputWriter, HangmanGame


class TestOutputWriter(OutputWriter):
    def __init__(self):
        self.state = None

    def write_output(self, state: State):
        self.state = state


class PenduTest(TestCase):
    def test_unexisting_letter(self):
        input_state = State(10, 'voiture', '*******')

        output = HangmanComputer().compute(input_state, 'y')

        self.assertEqual(output.coups, 9)
        self.assertEqual(output.guessed, '*******')

    def test_existing_letter(self):
        input_state = State(10, 'voiture', '*******')

        output = HangmanComputer().compute(input_state, 'o')

        self.assertEqual(output.coups, 10)
        self.assertEqual(output.guessed, '*o*****')

    def test_existing_letter2(self):
        input_state = State(10, 'voiture', '*******')

        output = HangmanComputer().compute(input_state, 'i')

        self.assertEqual(output.coups, 10)
        self.assertEqual(output.guessed, '**i****')

    def test_existing_letter_with_part_already_guessed(self):
        input_state = State(5, 'voiture', '***tur*')

        output = HangmanComputer().compute(input_state, 'v')

        self.assertEqual(output.coups, 5)
        self.assertEqual(output.guessed, 'v**tur*')

    def test_existing_letter_on_last_try(self):
        input_state = State(1, 'jeremy', '*e*em*')

        output = HangmanComputer().compute(input_state, 'y')

        self.assertEqual(output.coups, 1)
        self.assertEqual(output.guessed, '*e*emy')

    def test_double_found_letter(self):
        input_state = State(10, 'antidot', '*******')

        output = HangmanComputer().compute(input_state, 't')

        self.assertEqual(output.coups, 10)
        self.assertEqual(output.guessed, '**t***t')

    def test_no_more_tries(self):
        input_state = State(0, 'lambesc', 'l***es*')

        with self.assertRaises(ValueError):
            HangmanComputer().compute(input_state, 'q')


class PenduGameTest(TestCase):
    def setUp(self):
        self.reader = Mock()
        self.writer = Mock()
        self.computer = HangmanComputer()
        self.game = HangmanGame(self.reader, self.writer, self.computer)

    def test_basic_play(self):
        self.reader.read_input.return_value = 't'
        state = State(5, 'voiture', '*******')
        self.game.play(state)

        self.reader.read_input.assert_called_once_with()
        self.writer.write_output.assert_called_once_with(5, '***t***')

    def test_win(self):
        self.reader.read_input.return_value = 'e'
        state = State(10, 'voiture', 'voitur*')
        self.game.play(state)

        self.reader.read_input.assert_called_once_with()
        self.writer.win.assert_called_once_with()

    def test_lose(self):
        self.reader.read_input.return_value = 's'
        state = State(1, 'voiture', 'vo***re')
        self.game.play(state)

        self.reader.read_input.assert_called_once_with()
        self.writer.lose.assert_called_once_with('voiture')

    def test_already_won(self):
        self.reader.read_input.return_value = 'e'
        state = State(2, 'voiture', 'voiture')

        with self.assertRaises(ValueError):
            self.game.play(state)

        self.assertEqual(self.reader.read_input.call_count, 0)

    def test_already_lose(self):
        self.reader.read_input.return_value = 'e'
        state = State(0, 'voiture', 'v***ure')

        with self.assertRaises(ValueError):
            self.game.play(state)

        self.assertEqual(self.reader.read_input.call_count, 0)
