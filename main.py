import argparse
import os
import string
import sys
from time import sleep
from playwright.sync_api import sync_playwright

keyword_new = ["yeni", "YENİ", "Yeni", "YEni"]
keyword_torrent = ["torrent", "Torrent", "TORRENT"]
keyword_download = ["indir", "Alternatif", "LİNK", "Link", "Google", "Mega", "Mediafire"]


def get_game_by_search(search_string, page):
    os.system("cls")
    print("Searching for : " + search_string + "...")
    search_string = search_string.replace(" ", "+")
    page.goto("https://www.oyunindir.vip/?s=" + search_string)

    search_results = page.query_selector_all(
        "#td-outer-wrap > div.td-main-content-wrap.td-container-wrap > div > div.td-pb-row > div.td-pb-span8.td-main-content > div > div > div.item-details > h3.entry-title > a")

    print("Search Results : \n")
    for n, i in enumerate(search_results, 1):
        print(f"{n}. {i.inner_text()}")

    selected = input("Enter your choice >> ")
    selected = int(selected) - 1
    selected_url = search_results[selected].get_attribute("href")
    page.goto(selected_url)
    get_game_by_url(selected_url, page)


def get_game_by_url(url, page):
    os.system("cls")
    page.goto(url)
    game_title = page.query_selector("div > div > header > h1.entry-title").inner_text()
    game_title = string.capwords(game_title)

    print("Title: " + game_title + "\n")
    print("URL: " + page.url + "\n")

    links_list = []
    new_links = []
    torrent_links = []
    download_links = []

    links_list.append(page.query_selector_all("div > div.td-post-content > p > a"))
    links_list.append(page.query_selector_all("div > div.td-post-content > p > strong > a"))

    for links in links_list:
        for link in links:

            # link filtreleme

            for kn in keyword_new:
                if kn in link.inner_text():
                    new_links.append(link)
                    new_links = list(set(new_links))
            for kt in keyword_torrent:
                if kt in link.inner_text():
                    torrent_links.append(link)
                    torrent_links = list(set(torrent_links))
            for kdl in keyword_download:
                if kdl in link.inner_text():
                    download_links.append(link)
                    download_links = list(set(download_links))

    if len(new_links) > 0:
        print("Yeni Linkler :")
        for l in new_links:
            print(l.inner_text() + " >> " + l.get_attribute("href"))
        print("\n")

    if len(torrent_links) > 0:
        print("Torrent Linkleri :")
        for l in torrent_links:
            print(l.inner_text() + " >> " + l.get_attribute("href"))
        print("\n")

    print("İndirme Linkleri :")
    for l in download_links:
        print(l.inner_text() + " >> " + l.get_attribute("href"))
    print("\n")

    sleep(10)


def main():
    os.system("cls") if os.name == "nt" else os.system("clear")
    print("".center(50, "*"))
    print("     oyunindir-vip-scraper     ".center(50, "*"))
    print("".center(50, "*"))
    print("\n[1] Search Game")
    print("[2] Enter Game URL")
    print("[e] Exit")

    choice = input(">> ")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # headless=True demek GUI olmadan çalıştırmak
        page = browser.new_page()
        page.set_extra_http_headers({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

        if choice == "1":
            os.system("cls") if os.name == "nt" else os.system("clear")
            search_string = input("\n   [ Search Game ] >> ")
            os.system("cls") if os.name == "nt" else os.system("clear")
            get_game_by_search(search_string, page)

        elif choice == "2":
            os.system("cls") if os.name == "nt" else os.system("clear")
            url_input = input("\n   [ Game URL ] >> ")
            os.system("cls") if os.name == "nt" else os.system("clear")
            get_game_by_url(url_input, page)

        elif choice == "e":
            sys.exit(0)

        else:
            print("Invalid choice, please try again.")
            main()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--search", help="Search for specific game and get information about it.")
    parser.add_argument("-u", "--url", help="Enter game url and get download information.")
    args = parser.parse_args()
    if args.search:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.set_extra_http_headers({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            })
            get_game_by_search(args.search, page)
            browser.close()
    if args.url:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.set_extra_http_headers({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            })
            get_game_by_url(args.url, page)
            browser.close()
    else:
        main()
