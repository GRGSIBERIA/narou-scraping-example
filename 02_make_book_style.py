from selenium import webdriver
from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString
import json


def make_book_style(chapter_names, section_tags):
    book = {chap: [] for chap in chapter_names}

    chapid = -1
    for section in section_tags:
        url = section["href"]
        secname = section.string
        
        if "プロローグ" in secname:
            chapid += 1

        book[chapter_names[chapid]].append({"url": url, "name": secname})

    return book


if __name__ == "__main__":
    with open("./data/index.html", "r", encoding="utf-8") as html:
        soup = BeautifulSoup(html, "html.parser")

    index = soup.select_one("div.index_box")

    chapter_names = [chap.string for chap in index.select("div")]
    section_tags = index.select("a")
    book = make_book_style(chapter_names, section_tags)

    with open("./data/chapters.json", "w", encoding="utf-8") as js:
        json.dump(book, js, ensure_ascii=False)
        