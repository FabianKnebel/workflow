# get the first 10 google results for the query "Audiogästebuch"
import time
import re
import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


def get_google_results_selenium(query):
    url = "https://www.google.de/search?q=" + query
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("user-data-dir=C:\\Users\\Fabian Knebel\\AppData\\Local\\Google\\Chrome\\SeleniumProfil")
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, 3000)")
    time.sleep(2)
    driver.implicitly_wait(3)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    google_entries = soup.find_all("div", class_="MjjYud")
    #time.sleep(40)
    return google_entries


def process_results(results):
    data = []
    for result in results:
        rank = str(results.index(result) + 1)
        try:
            name = result.find("span", class_="VuuXrf").get_text()
        except Exception as e:
            if e.__class__.__name__ == "AttributeError":
                name = ""
                continue
        url = result.find("a", href=True)["href"]
        headline = result.find("h3").get_text()
        try:
            logo = result.find_all("img")[0]["src"]
        except Exception as e:
            if e == "IndexError":
                logo = ""
        try:
            img_id = re.findall(r"dimg[_\S*]*_\d+", str(result))[-1]
            preview = result.find("img", id=img_id)["src"]
        except Exception as e:
            if e == "IndexError":
                preview = ""
        try:
            text = result.find("div", class_="Z26q7c UK95Uc VGXe8").get_text()
        except Exception as e:
            if e.__class__.__name__ == "AttributeError":
                text = ""
        data += [[rank, name, url, headline, logo, preview, text]]
        print(rank + "\n" + name + "\n" + url + "\n" + headline + "\n" + text)

        print("---------------------------------------------------")
    return data



def write_to_csv(results):
    with open("analyze_google.csv", "a", encoding="utf-8") as file:
        new_data = process_results(results)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
        for row in new_data:
            # Time, Rank, Name, URL, Headline, Logo, Preview, Text
            file.write(timestamp + "," + row[0] + "," + row[1] + "," + row[2] + "," +
                       row[3] + "," + row[4] + "," + row[5] + "," + row[6] + "\n")


if __name__ == "__main__":
    google_results = get_google_results_selenium("Audiogästebuch")
    write_to_csv(google_results)