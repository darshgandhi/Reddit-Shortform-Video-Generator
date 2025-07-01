def sanitize_text(text):
    replacements = {
        "fuck": "frick",
        "fucking": "freaking",
    }

    for bad_word, replacement in replacements.items():
        text = text.replace(bad_word, replacement)
        text = text.replace(bad_word.capitalize(), replacement.capitalize())

    return text
