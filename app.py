from bs4 import BeautifulSoup
from urllib import request
from common import http_headers
from grabbers import moonwalk, sibnet, vk


def url_reader(url):
    req = request.Request(url, headers=http_headers.user_agent)
    html = request.urlopen(req)
    soup = BeautifulSoup(html.read(), 'html.parser')
    video_url = soup.find('iframe', {'id': 'film_main'})['src']
    playlist_url = ''
    if 'moonwalk' in video_url:
        playlist_url = moonwalk.grab_video(video_url)
    elif 'sibnet' in video_url:
        playlist_url = sibnet.grab_video(video_url)
    elif 'video_ext' in video_url:
        playlist_url = vk.grab_video(video_url)
    return playlist_url


if __name__ == '__main__':
    url_moonwalk = 'http://online.anidub.com/anime_tv/full/9197-ansatsu-kyoushitsu.html'
    url_sibnet = "http://online.anidub.com/anime_tv/anime_ongoing/9589-klass-ubiyc-tv-2-ansatsu-kyoushitsu-tv-2-01-iz-25.html"
    url_vk = "http://online.anidub.com/anime_tv/anime_ongoing/9747-prikaz-svyshe-big-order-01-iz-16.html"