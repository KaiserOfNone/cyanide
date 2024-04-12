from machine.turing import Direction, TuringMachine


def test_simple_step():
    tm = TuringMachine(
        alphabet=set(['a', 'b']),
        states=set(['q1']),
        delta={
            ('q1', 'a'): ('q1', 'b', Direction.LEFT)
        },
        start_state='q1',
        terminal_states=set(['q1']),
        ribbon='a'
    )
    tm.next_step()
    assert tm.get_ribbon() == 'b'

def test_move_back_alot():
    tm = TuringMachine(
        alphabet=set(['a', 'b']),
        states=set(['q1']),
        delta={
            ('q1', 'b'): ('q1', 'b', Direction.LEFT)
        },
        start_state='q1',
        terminal_states=set(['q1']),
        ribbon='a'
    )
    for i in range(10):
        tm.next_step()
    assert tm.get_ribbon() == 'a'

def test_prepend():
    tm = TuringMachine(
        alphabet=set(['a', 'b', '$']),
        states=set(['St', 'Fa', 'Fb', 'T']),
        delta={
            ('St', 'a'): ('Fa', '$', Direction.RIGHT),
            ('St', 'b'): ('Fb', '$', Direction.RIGHT),
            ('St', ' '): ('T', '$', Direction.LEFT),
            ('Fa', 'a'): ('Fa', 'a', Direction.RIGHT),
            ('Fa', 'b'): ('Fb', 'a', Direction.RIGHT),
            ('Fa', ' '): ('T', 'a', Direction.RIGHT),
            ('Fb', 'a'): ('Fa', 'b', Direction.RIGHT),
            ('Fb', 'b'): ('Fb', 'b', Direction.RIGHT),
            ('Fb', ' '): ('T', 'b', Direction.RIGHT),
            ('T', 'a'): ('T', 'a', Direction.LEFT),
            ('T', 'b'): ('T', 'b', Direction.LEFT),
            ('T', '$'): ('T', '$', Direction.LEFT),
            ('T', ' '): ('T', ' ', Direction.LEFT),
        },
        start_state='St',
        terminal_states=set(['T']),
        ribbon='abba'
    )
    for x in tm:
        print(x)
    assert tm.get_ribbon().strip() == '$abba'

def test_pretty_print():
    tm = TuringMachine(
        alphabet=set(['a', 'b']),
        states=set(['q1']),
        delta={
            ('q1', 'b'): ('q1', 'b', Direction.LEFT)
        },
        start_state='q1',
        terminal_states=set(['q1']),
        ribbon='abba'
    )
    expected = \
'''abba
^
q1'''
    assert tm.pretty_print() == expected
