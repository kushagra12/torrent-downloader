# torrent-downloader
Simple python scripts for lazy guys. Coded in python 2.

## Features

1. Download torrent without going to the torrent websites.
2. Download TV series with subtitles.
3. Get info of the TV Series when downloading it.
4. TV series are stored so next time you can quick select it later.
5. It stores the latest tv series episode, so it checks if no new episode has come and informs you accordingly.
6. Checks for low seeders (less than 10) and informs you accordingly.
7. Made completly torrent client and Os agnontic. Didn't check though :P
8. Some more cool stuff which I can't say without geeking out.

## How To Use
Download the repo as a zip.

Find the following line in findfile.py
```
self.baseTorrentSpace = "E:\\Downloads\\ff"
```
You need to change it to point it towards your own torrents download location.

Then you need to install BeautiFulSoup 4, Requests and pandas via pip.

Then open a terminal on the root of project and run torrent.py with python. Remember it only supports Python 2 for now.

```
$ python torrents.py
```
