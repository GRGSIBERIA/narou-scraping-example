import shutil
import json

if __name__ == "__main__":
    js = json.load(open("./data/chapters.json", "r", encoding="utf-8"))
    for chapter, _ in js.items():
        path = "./data/{}/build".format(chapter)
        shutil.make_archive(chapter, "zip", path)
        shutil.move("./{}.zip".format(chapter), "./{}.epub".format(chapter))