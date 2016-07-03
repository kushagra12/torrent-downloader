import base64
import os
import struct
import xmlrpclib
import zlib


class OpenSubtitlesAPI:
    def __init__(self):
        self.svc = xmlrpclib.ServerProxy('http://api.opensubtitles.org/xml-rpc')
        self.token = self.svc.LogIn("", "", "en", "OSTestUserAgent")['token']

    def download_subs(self, path, file_name):
        hashed_path = self.hash_file(os.path.join(path, file_name))

        subs_id = self.svc.SearchSubtitles(self.token, [{
            'tag': file_name,
            'sublanguageid': 'eng'
        }])['data'][0]['IDSubtitleFile']

        string = self.svc.DownloadSubtitles(self.token, [subs_id])['data'][0]['data']
        file_string_subtitles = base64.b64decode(string)

        return zlib.decompress(file_string_subtitles, 16 + zlib.MAX_WBITS)

    def get_details(self, path):
        hashed_path = self.hash_file(path)
        print self.svc.CheckMovieHash(self.token, [hashed_path])

    @staticmethod
    def hash_file(name):
        try:
            longlongformat = '<q'
            bytesize = struct.calcsize(longlongformat)

            f = open(name, "rb")

            filesize = os.path.getsize(name)
            hash = filesize

            if filesize < 65536 * 2:
                return "SizeError"

            for x in range(65536 / bytesize):
                buffer = f.read(bytesize)
                (l_value,) = struct.unpack(longlongformat, buffer)
                hash += l_value
                hash = hash & 0xFFFFFFFFFFFFFFFF

            f.seek(max(0, filesize - 65536), 0)
            for x in range(65536 / bytesize):
                buffer = f.read(bytesize)
                (l_value,) = struct.unpack(longlongformat, buffer)
                hash += l_value
                hash = hash & 0xFFFFFFFFFFFFFFFF

            f.close()
            returnedhash = "%016x" % hash
            return returnedhash

        except(IOError):
            return "IOError"
