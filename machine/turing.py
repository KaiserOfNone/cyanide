from enum import IntEnum


class Direction(IntEnum):
    LEFT = -1
    KEEP = 0
    RIGHT = 1


class TuringMachine:
    alphabet: set
    states: set
    delta: dict[tuple[str, str], tuple[str, str, Direction]]
    current_state: str
    terminal_states: set
    position: int
    ribbon: list
    halted: bool

    def __init__(self, alphabet, states, delta, start_state, terminal_states, ribbon):
        if start_state not in states:
            raise Exception(f"State {start_state} is not valid")
        for state in terminal_states:
            if state not in states:
                raise Exception(f"terminal {state} not in states")
        self.alphabet = alphabet
        self.states = states
        self.delta = delta
        self.current_state = start_state
        self.terminal_states = terminal_states
        self.position = 0
        self.halted = False
        self.ribbon = list(ribbon)

    def __iter__(self):
        return self

    def __next__(self):
        if self.halted:
            raise StopIteration
        self.next_step()
        return self.ribbon

    def extend_ribbon(self):
        self.ribbon = self.ribbon + [" "]

    def write(self, character):
        self.ribbon[self.position] = character

    def get_ribbon(self) -> str:
        return "".join(self.ribbon)

    def next_step(self):
        if self.halted:
            return
        character: str = self.ribbon[self.position]
        change = self.delta.get((self.current_state, character))
        if change is None:
            self.halted = True
            return
        new_state, new_character, direction = change
        if direction == Direction.RIGHT and self.position + 1 == len(self.ribbon):
            self.extend_ribbon()
        self.write(new_character)
        self.current_state = new_state
        self.position += direction
        if self.position == -1:
            self.halted = True

    def pretty_print(self):
        p = self.get_ribbon()
        p += "\n" + " " * self.position + "^"
        p += "\n" + " " * self.position + self.current_state
        return p
