import re

def normalize(in_string: str) -> str:
    """Replace cirilan symbils on latitians and change other to _ (except digit)

    Args:
        in_string (string):  need re module and use string translate
    """
    lation = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
              "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
    trans = {}
    for c, l in zip("абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ", lation):
        trans[ord(c)] = l
        trans[ord(c.upper())] = l.upper()

    return re.sub(r'[^0-9a-zA-Z]', '_', in_string.translate(trans))
