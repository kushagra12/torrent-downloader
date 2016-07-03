import requests
from bs4 import BeautifulSoup
import os
import re
import pandas as pd
import findfile
import time

initial_path = "https://kickass.unblocked.red/usearch/"
df_shows = pd.read_csv("shows.csv", parse_dates=True)
print df_shows
search_term = raw_input("Enter the search term or index value for TV show: ")

if search_term.isdigit():
    search_term = df_shows.loc[int(search_term), 'show']
    print "Searching for Latest Episode of " + search_term

search_obj = re.search(r'S[0-9]{2}E[0-9]{2}', search_term, re.I)
r = requests.get(initial_path + search_term)
soup = BeautifulSoup(r.content, 'html.parser')

flag = True

seeders = int(soup.find("table", "data").find_all("tr")[1].find("td", "green center").get_text())
torrent_name = str(soup.find("table", "data").find_all("tr")[1].find("a", "cellMainLink").get_text())

search_term = re.sub(' s[0-9]{2}e[0-9]{2}', "", search_term, flags=re.I)

if not search_obj:
    search_obj = re.search(r'S[0-9]{2}E[0-9]{2}', torrent_name, re.I)
    flag_for_saving = True
else:
    print "Downloading Specific Episode of " + search_term
    flag_for_saving = False

if search_obj:
    print "TV series Detected"
    episode_dwlded = df_shows.loc[df_shows.show == search_term, 'latest_episode']
    if episode_dwlded.values.size != 0:
        print "Latest Episode Downloaded: " + episode_dwlded.values[0]
        if episode_dwlded.values[0] == search_obj.group():
            print "Latest Episode Already There. Closing Now"
            flag = False
        else:
            if flag_for_saving:
                df_shows.set_value(df_shows.show == search_term, "latest_episode", search_obj.group())
    else:
        print "Adding New TV Series"
        df_shows.loc[-1] = [search_term, search_obj.group()]
        df_shows.index += 1
        df_shows = df_shows.sort_index()

if seeders > 10 and flag == True:
    magnet_link = soup.find_all("div", "iaconbox")[0].find_all("a", title="Torrent magnet link")[0].get("href")
    print "Downloading " + torrent_name
    os.startfile(magnet_link)
elif flag:
    prompt = raw_input("Not Enough Seeders\nSeeders: " + str(seeders) + "\nWant to continue (Y/N)")
    if prompt == 'Y' or prompt == 'y':
        magnet_link = soup.find_all("div", "iaconbox")[0].find_all("a", title="Torrent magnet link")[0].get("href")
        print "Downloading " + torrent_name
        os.startfile(magnet_link)

df_shows.to_csv("shows.csv", index=False)
print("Press any key to continue")
raw_input()

if search_obj:
    print "******************************************************"
    print "Now Downloading Subtitles"
    time.sleep(5)
    subs = findfile.FindFile()
    subs.find_file_and_dwld_subs(search_term, search_obj.group())
