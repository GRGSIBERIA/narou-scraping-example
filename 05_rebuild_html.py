import json
import os
import os.path
import glob
from bs4 import BeautifulSoup


def reshape_html(honbun):
    ps = honbun.select("p")
    lines = []
    for p in ps:
        if p.select_one("br"):
            pass
        else:
            if p.string != None:
                lines.append("<p>{}</p>\n".format(p.string))
    
    return lines
            


def rebuild_html(html_path, chapter):
    with open(html_path, "r", encoding="utf-8") as html:
        soup = BeautifulSoup(html, "html.parser")
    
    honbun = soup.select_one("div#novel_honbun")
    title = str(soup.select_one("title")).split("-")[-1].strip()
    basename = os.path.basename(html_path)

    rebuild_path = "./data/{}/build/{}".format(chapter, basename)

    lines = reshape_html(honbun)
    lines = "".join(lines)

    with open(rebuild_path, "w", encoding="utf-8") as html:
        text = [
            """<?xml version="1.0" encoding="UTF-8"?>""",
            "<!DOCTYPE html>",
            "<html lang=\"ja\">",
            "<head>",
            "<meta charset=\"UTF-8\" />",
            """<meta content="vertical-rl" name="primary-writing-mode" />""",
            """<link rel="stylesheet" href="main.css" type="text/css" />""",
            "<title>{}".format(title),
            "</head>",
            "<body>\n<h2>{}</h2>\n{}</body>".format(title.replace("</title>", ""), lines),
            "</html>"
            ]
        html.write("\n".join(text))



if __name__ == "__main__":
    js = json.load(open("./data/chapters.json", "r", encoding="utf-8"))

    for chapter, sections in js.items():
        path = "./data/{}/build".format(chapter)
        if not os.path.exists(path):
            os.mkdir(path)
        html_pathes = glob.glob("./data/{}/src/*.html".format(chapter))

        for html_path in html_pathes:
            rebuild_html(html_path, chapter)
