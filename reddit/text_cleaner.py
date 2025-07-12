import re

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
    return text