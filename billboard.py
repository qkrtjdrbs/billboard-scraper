import requests
import webbrowser
from bs4 import BeautifulSoup
from tkinter import *

win = Tk()

win.iconbitmap('./icon.ico')
win.geometry("1000x1000")
win.title("Billboard")

sb = Scrollbar(win, orient=VERTICAL)
sb.pack(side=RIGHT, fill=Y)

lb = Listbox(win, height=500, width=1000, font=('Times', 14))
lb.pack()

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
}

URL = "https://www.billboard.com/charts/hot-100"

result = requests.get(URL, headers=headers)
soup = BeautifulSoup(result.text, "html.parser")
songs = soup.find_all("div", {"class": "o-chart-results-list-row-container"})
weekend = soup.find(
    "p", {"class": "a-font-primary-medium-xs"}).get_text()


def extract_song(html):
    rank = html.find(
        "span", {"class": "a-font-primary-bold-l"}).get_text()
    title = html.find(
        "h3", {"class": "c-title"}).get_text()
    artist = html.find(
        "span", {"class": "a-font-primary-s"}).get_text()
    searchTitle = title.replace(" ", "+")
    searchArtist = artist.replace(" ", "+")
    link = f"https://www.youtube.com/results?search_query={searchTitle}+{searchArtist}"
    return {
        'rank': rank,
        'title': title,
        'artist': artist,
        'link': link
    }


def extract_songs():
    songsInfos = []
    for song in songs:
        songsInfo = extract_song(song)
        songsInfos.append(songsInfo)
    lb.insert(END, weekend, "")
    for songInfo in songsInfos:
        lb.insert(END, f"Rank {songInfo['rank']}", songInfo['title'],
                  songInfo['artist'], songInfo['link'], "")


def internet(event):
    weblink = lb.get(ACTIVE)
    webbrowser.open(weblink)


lb.bind("<Double-1>", internet)

sb.configure(command=lb.yview)
lb.configure(yscrollcommand=sb.set)


extract_songs()
win.mainloop()
