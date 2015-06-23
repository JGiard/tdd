import string


def diamond_line(inside, outside, letter):
    """print a diamond line with specified padding"""
    if inside <= 0:
        return ' '*outside + letter + ' '*outside
    return ' '*outside + letter + ' '*inside + letter + ' '*outside


def previous_letter(letter):
    """return previous letter in alphabet"""
    index = string.ascii_uppercase.find(letter)
    return string.ascii_uppercase[index - 1]


def half_diamond_rec(inside, outside, letter):
    """recursively build half of a diamond"""
    if letter == 'A':
        return [diamond_line(inside, outside, letter)]

    up_diamond = half_diamond_rec(inside - 2, outside + 1, previous_letter(letter))
    current_line = diamond_line(inside, outside, letter)
    return up_diamond + [current_line]


def assemble_diamond(diamond_size, letter):
    up_diamond = half_diamond_rec(diamond_size - 2, 1, previous_letter(letter))
    down_diamond = list(reversed(up_diamond))
    middle_diamond = diamond_line(diamond_size, 0, letter)
    return up_diamond + [middle_diamond] + down_diamond


def diamond(letter: str):
    letter = letter.upper()
    if letter == 'A':
        return ['A']
    letter_num = string.ascii_uppercase.find(letter) + 1
    diamond_size = (letter_num - 1) * 2 - 1

    return assemble_diamond(diamond_size, letter)


def nice_diamond(letter: str):
    return '\n'.join(diamond(letter))


if __name__ == "__main__":
    print(nice_diamond('A'))
    print(nice_diamond('B'))
    print(nice_diamond('C'))
    print(nice_diamond('D'))
    print(nice_diamond('E'))
    print(nice_diamond('F'))
