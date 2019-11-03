import shutil
import json

if __name__ == "__main__":
    js = json.load(open("./data/chapters.json", "r", encoding="utf-8"))
    for chapter, _ in js.items():
        dest = "./data/{}/build/cover.jpg".format(chapter)
        source = "./data/cover.jpg"
        shutil.copy(source, dest)

        dest = "./data/{}/build/main.css".format(chapter)
        source = "./data/main.css"
        shutil.copy(source, dest)