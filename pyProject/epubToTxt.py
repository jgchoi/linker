import epub_conversion
from epub_conversion.utils import open_book, convert_epub_to_lines
from bs4 import BeautifulSoup


def epub_to_txt(epub_path):
    # open epub_file, extract all texts, return texts
    book = open_book(epub_path)
    lines = convert_epub_to_lines(book)
    text = '\n'.join(lines)
    soup = BeautifulSoup(text, 'html.parser')
    text = soup.get_text()

    return text

def write_to_txt(text, txt_path):
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(text)

# Usage
