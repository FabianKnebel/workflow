# get the first 10 google results for the query "Audiogästebuch"
import time

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
    driver.execute_script("window.scrollTo(0, 1080)")
    driver.execute_script("window.scrollTo(0, 2160)")
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    google_entries = soup.find_all("div", class_="MjjYud")
    time.sleep(40)
    return google_entries


def process_results(results):
    data = []
    for result in results:
        print(result)
        try:
            rank = results.index(result) + 1
            name = result.find("span", class_="VuuXrf").get_text()
            url = result.find("a", href=True)["href"]
            headline = result.find("h3").get_text()
            print(result.find_all("img"))
            logo = result.find_all("img")[0]["src"]
            preview = result.find_all("img")[1]["src"]
            text = result.find("div", class_="Z26q7c UK95Uc VGXe8").get_text()
            data += [[rank, name, url, headline, logo, preview, text]]
            print(str(rank) + "\n" + name + "\n" + url + "\n" + headline + "\n" + text)
        except exception as e:
            if e == "AttributeError":
                print("AttributeError")
            elif e == "IndexError":
                print("IndexError")
            else:
                print(e)
        print("---------------------------------------------------")
    return data



def write_to_csv(results):
    with open("analyze_google.csv", "a", encoding="utf-8") as file:
        new_data = process_results(results)
        for row in new_data:
            file.write(str(row) + "\n")


if __name__ == "__main__":
    google_results = get_google_results_selenium("Audiogästebuch")
    write_to_csv(google_results)