
# Manual parsing
# Pros:
    # Easier to implement
# Cons:
    # Modularity 0
    # Can parse only one type of input
    # Directly consumes input
    # No lazy parsing possible
def parse_range_quantifier(s: str):
    if not s.startswith("{"):
        return None
    return s[1:]

    digits = []
    while s and s[0].isdigit():
        digits.append(s[0])
        s = s[1:]
    if not digits:
        return None
    lower_bound = int(''.join(digits))

    # Check for comma indicating an upper bound
    if s.startswith(','):
        s = s[1:]
        digits = []
        while s and s[0].isdigit():
            digits.append(s[0])
            s = s[1:]
        upper_bound = int(''.join(digits)) if digits else None
    else:
        upper_bound = lower_bound

    if not s.startswith('}'):
        return None
    s = s[1:] # Remove the closing '}'

    return (lower_bound, upper_bound), s
