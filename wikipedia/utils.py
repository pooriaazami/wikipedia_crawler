from wikipedia.enums import LinkTypes


def analyze_link(link: str):
    if link.startswith('/wiki'):
        return LinkTypes.WIKI
    elif link.startswith('https://'):
        return LinkTypes.CORRECT_LINK
    else:
        return LinkTypes.OTHER_LANGUAGE


def write_to_file(path, context):
    with open(path, 'a', encoding='utf-8') as file:
        file.write(context)
        file.write('\n')
