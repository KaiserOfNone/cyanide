import click
import toml
import time

from machine.turing import TuringMachine, Direction, parse_direction

def parse_delta(list) -> dict[tuple[str, str], tuple[str, str, Direction]]:
    delta = {}
    for row in list:
        if len(row) != 2:
            raise Exception(f"Malformed delta entry: {row}")
        arg, pred = row
        if len(arg) != 2:
            raise Exception(f"Malformed argument for delta: {arg}")
        original_state, character = arg
        if len(pred) != 3:
            raise Exception(f"Malformed predicate for delta: {pred}")
        new_state, new_character, direction_string = pred
        direction = parse_direction(direction_string)
        delta[(original_state, character)] = (new_state, new_character, direction)
    return delta

@click.command()
@click.option("--machine-def", default="./machine.toml", help="The machine definition file (read the docs)")
@click.option("--ribbon", default="", help="The ribbon to run the machine with")
@click.option("--speed", default=16, help="Wait time between iterations for display (in milliseconds)")
@click.option("--max-iters", default=1000, help="Max iterations to do, set -1 for infinite.")
def main(machine_def, ribbon, speed, max_iters):
    settings = {}
    with open(machine_def, "r") as f:
        settings = toml.load(f)
    alphabet = set(settings["alphabet"])
    states = set(settings["states"])
    delta = parse_delta(settings["delta"])
    start_state = settings["start_state"]
    terminal_states = set(settings["terminal_states"])
    ms_sleep = speed/1000

    tm = TuringMachine(
        alphabet=alphabet,
        states=states,
        delta=delta,
        start_state=start_state,
        terminal_states=terminal_states,
        ribbon=ribbon,
    )
    if max_iters == -1:
        while tm:
            print(tm.pretty_print())
            time.sleep(ms_sleep)
    else:
        for i in range(max_iters):
            if tm.halted:
                break
            tm.next_step()
            print(tm.pretty_print())
            time.sleep(ms_sleep)

if __name__ == "__main__":
    main()
