import json
import os.path
import os
from selenium import webdriver

if __name__ == "__main__":
    driver = webdriver.Chrome()
    js = json.load(open("./data/chapters.json", "r", encoding="utf-8"))
    
    for chapter_name, sections in js.items():
        path = "./data/{}".format(chapter_name)
        if not os.path.exists(path):
            os.mkdir(path)
        
        for section in sections:
            sid = section["url"].split("/")[-2]
            url = section["url"]
            name = section["name"]
            
            driver.get("https://ncode.syosetu.com/{}".format(url))
            html = driver.page_source
            with open("{}/{}.html".format(path, sid), "w", encoding="utf-8") as f:
                f.write(html)
    
    driver.quit()