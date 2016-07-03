import os
import re
import opensubtitles


class FindFile:
    def __init__(self):
        # You need to change this to your Torrent Download Directory
        self.baseTorrentSpace = "E:\\Downloads\\ff"

    def find_file_and_dwld_subs(self, searchterm, episode):
        torrent_list = os.listdir(self.baseTorrentSpace)

        searchterm = searchterm.replace(' ', '.')

        p = re.compile(r'' + searchterm + '(.*)' + episode, re.IGNORECASE)

        file_tv_dwld = ''

        for ford in torrent_list:
            if re.search(p, ford):
                if os.path.isdir(os.path.join(self.baseTorrentSpace, ford)):
                    self.baseTorrentSpace = os.path.join(self.baseTorrentSpace, ford)
                    sub_torrent_list = os.listdir(self.baseTorrentSpace)
                    for file_tv in sub_torrent_list:
                        if re.search(p, file_tv):
                            file_tv_dwld = file_tv
                            break
                else:
                    file_tv_dwld = ford
                break

        subtitles_file_name = re.sub(r'\.(mkv|mp4|avi)$', '.srt', file_tv_dwld)
        print subtitles_file_name

        api = opensubtitles.OpenSubtitlesAPI()

        # api.get_details(os.path.join(baseTorrentSpace, file_tv_dwld))
        subs = api.download_subs(self.baseTorrentSpace, file_tv_dwld)

        if subs != '':
            f = open(os.path.join(self.baseTorrentSpace, subtitles_file_name), mode='w')
            f.write(subs)
            f.close()
