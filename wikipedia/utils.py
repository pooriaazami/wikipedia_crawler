from wikipedia.enums import LinkTypes


def analyze_link(link: str):
    if not link.startswith('https://'):
        return LinkTypes.CORRECT_LINK
    else:
        return LinkTypes.OTHER_LANGUAGE
