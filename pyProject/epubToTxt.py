import os
from ebooklib import epub
from bs4 import BeautifulSoup

def epub_to_txt(epub_path):
    book = epub.read_epub(epub_path)
    text = ""

    for item in book.get_items():
        if isinstance(item, epub.EpubHtml):
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            text += soup.get_text() + "\n"

    return text

def write_to_txt(text, txt_path):
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(text)

# Usage
