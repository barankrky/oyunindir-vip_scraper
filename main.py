import os, argparse, string
from undetected_chromedriver import Chrome
from time import sleep
from selenium.webdriver.common.by import By

driver = Chrome()


keyword_new = ["yeni", "YENİ", "Yeni", "YEni"]
keyword_torrent = ["torrent", "Torrent", "TORRENT"]
keyword_download = ["indir", "Alternatif", "LİNK", "Link", "Google", "Mega", "Mediafire"]

def getGameBySearch(search_string):
    os.system("cls")
    print("Searching for : " + search_string + "...")
    search_string = search_string.replace(" ", "+")
    driver.get("https://www.oyunindir.vip/?s=" + search_string)

    search_results = driver.find_elements(By.CSS_SELECTOR, value="#td-outer-wrap > div.td-main-content-wrap.td-container-wrap > div > div.td-pb-row > div.td-pb-span8.td-main-content > div > div > div.item-details > h3.entry-title > a")

    print("Search Results : \n")
    n = 1
    for i in search_results:
        print(f"{n}. {i.text}")
        n = n + 1
    selected = input("Enter your choice >> ")
    selected = int(selected) - 1
    selected_url = search_results[selected].get_attribute("href")
    driver.get(selected_url)
    getGameByURL(selected_url)



def getGameByURL(url):
    os.system("cls")
    driver.get(url)
    game_title = driver.find_element(by=By.CSS_SELECTOR, value="div > div > header > h1.entry-title").text
    game_title = string.capwords(game_title)

    print("Title: " + game_title + "\n")
    print("URL: " + driver.current_url + "\n")

    links_list = []
    new_links = []
    torrent_links = []
    download_links = []

    links_list.append(driver.find_elements(by=By.CSS_SELECTOR, value="div > div.td-post-content > p > a"))
    links_list.append(driver.find_elements(by=By.CSS_SELECTOR, value="div > div.td-post-content > p > strong > a"))

    for links in links_list:
        for link in links:

            # link filtreleme

            for kn in keyword_new:
                if kn in link.text:
                    new_links.append(link)
                    new_links = list(set(new_links))
            for kt in keyword_torrent:
                if kt in link.text:
                    torrent_links.append(link)
                    torrent_links = list(set(torrent_links))
            for kdl in keyword_download:
                if kdl in link.text:
                    download_links.append(link)
                    download_links = list(set(download_links))


    if len(new_links) > 0:
        print("Yeni Linkler :")
        for l in new_links:
            print(l.text + " >> " + l.get_attribute("href"))
        print("\n")

    if len(torrent_links) > 0:
        print("Torrent Linkleri :")
        for l in torrent_links:
            print(l.text + " >> " + l.get_attribute("href"))
        print("\n")

    print("İndirme Linkleri :")
    for l in download_links:
        print(l.text + " >> " + l.get_attribute("href"))
    print("\n")


    sleep(10)


parser = argparse.ArgumentParser()
parser.add_argument("-s", "--search", help="Search for specific game and get information about it.")
parser.add_argument("-u", "--url", help="Enter game url and get download information.")
args = parser.parse_args()
if args.search:
    getGameBySearch(args.search)
if args.url:
    getGameByURL(args.url)




