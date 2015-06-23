class State:
    def __init__(self, coups, mot, guessed):
        self.coups = coups
        self.mot = mot
        self.guessed = guessed

    def __eq__(self, other):
        return self.coups == other.coups and self.mot == other.mot and self.guessed == other.guessed

    def __str__(self):
        return '<State({},{},{})>'.format(self.coups, self.mot, self.guessed)


class HangmanComputer:
    def compute(self, state: State, letter: str) -> State:
        if state.coups == 0:
            raise ValueError('no more tries available')
        if letter not in state.mot:
            return State(state.coups - 1, state.mot, state.guessed)
        else:
            guessed = list(state.guessed)
            for i, c in enumerate(state.mot):
                if letter == c:
                    guessed[i] = letter
            guessed = ''.join(guessed)
            return State(state.coups, state.mot, guessed)


class InputReader:
    def read_input(self) -> str:
        pass


class OutputWriter:
    def write_output(self, coups, guessed):
        pass

    def win(self):
        pass

    def lose(self, solution):
        pass


class HangmanGame:
    def __init__(self, reader: InputReader, writer: OutputWriter, computer: HangmanComputer):
        self.reader = reader
        self.writer = writer
        self.computer = computer

    def check_state(self, state):
        if state.mot == state.guessed:
            raise ValueError('you have already won')
        if state.coups == 0:
            raise ValueError('you have already lost')

    def write_result(self, new_state):
        if new_state.guessed == new_state.mot:
            self.writer.win()
        elif new_state.coups == 0:
            self.writer.lose(new_state.mot)
        else:
            self.writer.write_output(new_state.coups, new_state.guessed)

    def play(self, state: State):
        self.check_state(state)
        letter = self.reader.read_input()
        new_state = self.computer.compute(state, letter)
        self.write_result(new_state)