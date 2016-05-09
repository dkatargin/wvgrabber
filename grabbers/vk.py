from urllib import request
from common import http_headers


def grab_video(video_url):
    real_vk_url_end = video_url.split('/')[-1]
    video_url = "http://vk.com/"+real_vk_url_end
    req = request.Request(video_url, headers=http_headers.user_agent)
    url_data = request.urlopen(req)
    return __get_playlist(url_data)


def __get_playlist(url_data):
    result = b''
    for l in url_data.readlines():
        if b'.mp4' in l:
            result = l
        else: continue
    raw_urls = [u.split(b'?')[0].replace(b'\\', b'').decode('UTF-8') for u in result.split(b'{', 1)[1].rsplit(b'}', 1)[0].split(b',') if b'url' in u and b'current' not in u]
    return raw_urls