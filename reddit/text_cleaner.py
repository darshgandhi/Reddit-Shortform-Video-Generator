import re

replacements = {
    "NTAH": "Not the A-hole",
    "NTA": "Not the A-hole",
    "YTAH": "You're the A-hole",
    "YTA": "You're the A-hole",
    "ESH": "Everyone Sucks Here",
    "NAH": "No A-holes Here",
    "INFO": "Not Enough Info",
    "YWBTAH": "You Would Be the A-hole",
    "YWBTA": "You Would Be the A-hole",
    "YWNBTAH": "You Would Not Be the A-hole",
    "YWNBTA": "You Would Not Be the A-hole",
    }

def sanitize_text(text):
    replacements = {
        "fuck": "frick",
        "fucking": "freaking",
    }

    for bad_word, replacement in replacements.items():
        text = text.replace(bad_word, replacement)
        text = text.replace(bad_word.capitalize(), replacement.capitalize())

    return text

def clean_comment(comment):
    backslash_pattern = re.compile(r"\\(\S+)")
    cleanup_pattern = re.compile(r'[^a-zA-Z0-9._-]')

    text = backslash_pattern.sub("", comment.body)
    text = text.replace("\n", " ")
    text = cleanup_pattern.sub(" ", text)
    text = re.sub(r'\s+', ' ', text).strip()

    for abbr, full in replacements.items():
        text = text.replace(abbr, full)

    return text