import requests
from selenium import webdriver

if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.get("https://ncode.syosetu.com/n4830bu/")
    html = driver.page_source
    with open("./data/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    driver.quit()
    