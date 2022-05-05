"""Terms common to many pipelines."""
from traiter import const as t_const

CONJ = ["or", "and"]
TO = ["to"]
MISSING = """
    without missing lack lacking except excepting not rarely obsolete
    """.split()

COMMON_PATTERNS = {
    "(": {"TEXT": {"IN": t_const.OPEN}},
    ")": {"TEXT": {"IN": t_const.CLOSE}},
    "-": {"TEXT": {"IN": t_const.DASH}, "OP": "+"},
    "-*": {"TEXT": {"IN": t_const.DASH}, "OP": "*"},
    "[+]": {"TEXT": {"IN": t_const.PLUS}},
    "/": {"TEXT": {"IN": t_const.SLASH}},
    ",": {"TEXT": {"IN": t_const.COMMA}},
    ".": {"TEXT": {"IN": t_const.DOT}},
    "x": {"TEXT": {"IN": t_const.CROSS}},
    ":": {"TEXT": {"IN": t_const.COLON}},
    "to": {"LOWER": {"IN": TO}},
    "-/or": {"LOWER": {"IN": t_const.DASH + TO + CONJ}, "OP": "+"},
    "-/to": {"LOWER": {"IN": t_const.DASH + TO}, "OP": "+"},
    "and/or": {"LOWER": {"IN": CONJ}},
    "missing": {"LOWER": {"IN": MISSING}},
    "9": {"IS_DIGIT": True},
    "99.9": {"TEXT": {"REGEX": t_const.FLOAT_TOKEN_RE}},
    "99-99": {"ENT_TYPE": "range"},
    "99.9-99.9": {"ENT_TYPE": "range"},
}