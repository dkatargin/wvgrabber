from common import http_headers
from urllib import request
from bs4 import BeautifulSoup

def get_titles(url):
    req = request.Request(url, headers=http_headers.user_agent)
    html = request.urlopen(req)
    soup = BeautifulSoup(html.read(), 'html.parser')
    series = soup.find_all("div", { "class" : "title" })
    for s in series:
        print(s.a['href'], s.a.contents[0])

if __name__ == '__main__':
    get_titles("http://online.anidub.com/")