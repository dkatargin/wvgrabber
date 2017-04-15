from urllib import request
from common import http_headers


def grab_video(video_url):
    req = request.Request(video_url, headers=http_headers.user_agent)
    url_data = request.urlopen(req)
    return __get_playlist(url_data)


def __get_playlist(url_data):
    playstr = b''
    for l in url_data.readlines():
        if b'.m3u8' in l:
            playstr = l
        else:
            continue
    playlist_url_end = [i for i in playstr.split(b',') if b'm3u8' in i][0].split(b':')[1].decode('utf-8').strip().replace('\'', '').replace('\"', '')
    playlist_url = "http://video.sibnet.ru"+playlist_url_end
    return playlist_url