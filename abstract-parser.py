class Parser:
    def __init__(self, parse_function) -> None:
        self.parse = parse_function

    def __call__(self, s):
        return self.parse(s)

    def map(self, func):
        return Parser(lambda s: self._map(s, func))

    def _map(self, s, func):
        result = self.parse(s)
        if result is None:
            return None
        value, rest = result
        return func(value), rest

    def flat_map(self, func):
        return Parser(lambda s: self._flat_map(s, func))

    def _flat_map(self, s, func):
        result = self.parse(s)
        if result is None:
            return None
        value, rest = result
        return func(value).parse(rest)

    def filter(self, predicate):
        return Parser(lambda s: self._filter(s, predicate))

    def _filter(self, s, predicate):
        result = self.parse(s)
        if result is None:
            return None
        value, rest = result
        if predicate(value):
            return value, rest
        return None

# EXCERCISES

## Excercise 1: Make a digit parser
digit_parser = Parser(lambda s: (s[0], s[1:]) if s and s[0].isdigit() else None)

## Output
print(digit_parser("1"))

## Excercise 2: Make an int Parser
### An int parser is just a digit parser, which converts a digit string into an integer

### Using this logic, rather than making an int parser from scratch;
### we derive an int parser from a digit parser snd use it:
int_parser = digit_parser.map(int)

## Output
print(int_parser("5abc"))

## Excercise 3: Alphabet parser
alpha_parser = Parser(lambda s: (s[0], s[1:]) if s and s[0].isalpha() else None)

## Output:
print(alpha_parser("a"))

## Excercise 4: String Parser
### This is redundant, yes, as char and strings are alike in python. But still, deriving a string parser from an existing alpha parser would look like:
string_parser = alpha_parser.map(str)

## Output:
print(string_parser("abc"))

## Excercise 5: Two digit parsing
### Instead of making a separate parser, try dynamically combining the parsers. We already have a digit parser.
### If we combine it with another digit parser. We get a double digit Parser
two_digit_parser = digit_parser.flat_map(lambda first: digit_parser.map(lambda second: (first, second)))

## Output:
print(two_digit_parser("56abc"))

## Excercise 5: Letter and a digit parser
### Here, we can dynamically combine an alpha parser witha a digit parser
letter_digit_parser = alpha_parser.flat_map(lambda first: digit_parser.map(lambda second: (first, second)))

### Output:
print(letter_digit_parser("a5bc"))

## Excercise 6: Specific letter parsing
### Here, we could have done something as such:
dedicated_letter_parser = Parser(lambda s: (s[0], s[1:]) if s and s[0] == "a" else None)

### But why don't you try reusing an existing Parser?
dedicated_letter_parser = alpha_parser.filter(lambda c: c == "a")

## Output:
print(dedicated_letter_parser("abc"))

## Excercise 7: Parse an entire word
### We do not have any form of basic parser which can parse an entire word
def word_parser(s):
    if not s or not s[0].isalpha():
        return None

    word = ""
    while s and s[0].isalpha():
        word += s[0]
        s = s[1:]

    return word, s

_word_parser = Parser(word_parser)

## Output:
print(_word_parser("hello123"))
print(_word_parser("abc"))
print(_word_parser("123"))

## Excercise 8: Parsing multiple digits
### Again, we fall short on such a Parser. Therefore, we must make one.
def n_digit_parse(s):
    if not s or not s[0].isdigit():
        return None

    num = ""
    while s and s[0].isdigit():
        num+=s[0]
        s = s[1:]

    if not num:
        return None

    return int(num), s

num_parser = Parser(n_digit_parse)

## Output:
print(num_parser("1234"))
print(num_parser("123abc"))

## Excercise 9: Parse a combination of digits following characters
### Hold your horses, isalnum() will work, yes. But, you already have both the parsers, try combining them.

word_then_number_parser = _word_parser.flat_map(lambda first: num_parser.map(lambda second: (first, second)))

## Output:
print(word_then_number_parser("abc123"))

## Excercise 10: Parse a combination of characters followings digits

number_then_word_parser = num_parser.flat_map(lambda first: _word_parser.map(lambda second: (first, second)))

## Output:
print(number_then_word_parser("123abc"))

## Excercise 11: Parse an alphanumeric string
### isalnum() is a plausible option here
### Complete this
