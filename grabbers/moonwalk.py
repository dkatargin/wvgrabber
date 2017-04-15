import base64
from bs4 import BeautifulSoup
from urllib import request, parse
import json
from common import http_headers


def grab_video(video_url):
    video_url = video_url.replace('mooonwalk.co', 'moonwalk.cc')
    req = request.Request(video_url, headers=http_headers.user_agent)
    url_data = request.urlopen(req)
    session_url = 'http://moonwalk.cc/sessions/create_session'
    post_data, csrf_raw, content_data = __get_post_data(url_data)
    post_dict = {}
    for d in post_data:
        key_item = d.split(':')[0]
        if key_item == 'cd':
            post_dict['cd'] = 0
            continue
        elif key_item == 'partner':
            post_dict['partner'] = ''
            continue
        val_item = ''.join(d.split(key_item))[1:].strip()
        post_dict[key_item] = val_item.replace('\'', '')
    post = request.Request(session_url, data=parse.urlencode(post_dict).encode('UTF-8'))
    post.add_header('Host', 'moonwalk.cc')
    post.add_header('Connection', 'keep-alive')
    post.add_header('Origin', 'http://moonwalk.cc')
    post.add_header('X-CSRF-Token', csrf_raw)
    post.add_header('User-Agent', http_headers.user_agent['User-Agent'])
    post.add_header('Content-type', 'application/x-www-form-urlencoded; charset=UTF-8')
    post.add_header('Accept', '*/*')
    post.add_header('X-Requested-With', 'XMLHttpRequest')
    post.add_header('Content-Data', base64.b64encode(content_data).decode('UTF-8'))
    post.add_header('DNT', 1)
    post.add_header('Referer', video_url)
    post.add_header('Accept-Encoding', 'gzip, deflate')
    post.add_header('Accept-Language', 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4')
    post.add_header('Cookie', '')
    playlist_data = request.urlopen(post)
    main_playlist_url = json.loads(playlist_data.read().decode('UTF-8'))['manifest_m3u8']
    playlist_req = request.Request(main_playlist_url, headers=http_headers.user_agent)
    playlist = request.urlopen(playlist_req)
    result_playlist_data = playlist.read().decode('UTF-8').split('\n')[-2]
    playlist_result = result_playlist_data.replace('#EXT-X-STREAM-INF:', '').strip()
    return playlist_result


def __get_post_data(url_data):
    post_data = []
    start_parse = False
    ContentData = ''
    html = b''
    for l in url_data.readlines():
        html += l
        if b'setRequestHeader|' in l:
            ContentData = l.decode('UTF-8')
            continue
        if b'/sessions/create_session' in l:
            start_parse = True
            continue
        else:
            if start_parse and b'success' not in l:
                post_data.append(l)
            else:
                if b'succes' in l:
                    start_parse = False
                    continue
                else:
                    continue

    cd = ''.join(ContentData.split('setRequestHeader|')[1:]).split('|beforeSend')[0].encode('UTF-8')
    csrf_soup = BeautifulSoup(html, 'html.parser')
    csrf = csrf_soup.find('meta', {'name': 'csrf-token'})['content']
    return [p.decode('utf-8').replace(',','').replace('\n','').strip() for p in post_data], csrf, cd