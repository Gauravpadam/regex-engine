from state import State, Transition, MatchChar, AnyCharacter
from cursor import Cursor

# I'm making a basic FSM here, for the grammar G = ab
start_state = State()
state_a = State()
accept_state = State()

start_state.transition.append(Transition(state_a, MatchChar('a')))
state_a.transition.append(Transition(accept_state, MatchChar('b')))

def run_FSM(start_state: State, input_string: str) -> bool:
    cursor: Cursor = Cursor(input_string)
    current_state: State = start_state

    # Here, we start the state machine

    while not cursor.is_empty:
        for transition in current_state.transition:

            result = transition.condition.can_perform_transition(cursor)
            if result.accepted:
                cursor.advance_to(cursor.index + result.count)
                current_state = transition.end
                break
        else:
            return False
    
    return current_state == accept_state

test_cases = ["ab", "a", "b", "abc", "abab"]

results = [run_FSM(start_state, test_case) for test_case in test_cases]

# print(results)

# What if you want to make it for grammar G = "a" "b" X*, X = AnyCharacter

# Clearing all previous transactions
start_state.transition.clear()
state_a.transition.clear()
accept_state.transition.clear()

# Setting new stats
start_state.transition.append(Transition(state_a, MatchChar('a')))
state_a.transition.append(Transition(accept_state, MatchChar('b')))

# Anything beyond ab transitions to accepting state
accept_state.transition.append(Transition(accept_state, AnyCharacter(including_newline=True)))

results = [run_FSM(start_state, test_case) for test_case in test_cases]

print(results)





