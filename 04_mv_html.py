import os
import os.path
import json
import shutil
import glob

if __name__ == "__main__":
    js = json.load(open("./data/chapters.json", "r", encoding="utf-8"))

    for chapter, sections in js.items():
        path = "./data/{}/src".format(chapter)
        if not os.path.exists(path):
            os.mkdir(path)
        
        html_pathes = glob.glob("./data/{}/*.html".format(chapter))
        
        for html_path in html_pathes:
            basename = os.path.basename(html_path)
            shutil.move(html_path, "{}/{}".format(path, basename))
