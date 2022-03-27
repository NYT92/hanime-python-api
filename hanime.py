# Credit to https://github.com/Profility/hanime-scraper


from bs4 import BeautifulSoup
import requests

base_url = "https://hanime.tv"
base_video_url = "https://hanime.tv/videos/hentai/"

def info(id: str) -> dict:
    response = requests.get(base_video_url + id).text
    soup = BeautifulSoup(response, 'lxml')
    info = soup.find_all('div', attrs=['class', 'hvpimbc-text grey--text'])
    brand = soup.find('a', attrs=['class', 'hvpimbc-text'])
    branduploads = None
    releasedate = None
    uploaddate = None
    alternatetitles = []
    views = soup.find('div', attrs=['class', 'tv-views grey--text']).text
    censorship = soup.find('a', attrs=['class', 'hvpimbc-censorship-btn'])
    status = bool
    if censorship.text == "CENSORED":
        status = True
    else:
        status = False

    for alttitle in soup.find_all('span', attrs=['class', 'mr-3 grey--text']):
        alternatetitles.append(alttitle.text)

    for count, info in enumerate(info):
        if count == 0:
            branduploads = info.text
        if count == 1:
            releasedate = info.text
        if count == 2:
            uploaddate = info.text
        if count == 3:
            break

    return {
        'brand': brand.text,
        'branduploads': branduploads,
        'releasedate': releasedate,
        'uploaddate': uploaddate,
        'views': views,
        'censored': status,
        'alternatetitles': alternatetitles
    }

def description(id : str) -> str:
    response = requests.get(base_video_url + id).text
    soup = BeautifulSoup(response, 'lxml')

    description = soup.find('div', attrs=['class', 'mt-3 mb-0 hvpist-description'])
    fulldesc = []

    for desc in description.findChildren():
        f1 = str(desc).replace('<p>', '')
        f2 = f1.replace('</p>', '')
        fulldesc.append(f2)

    return ''.join(fulldesc)

def poster(id: str) -> str:
    response = requests.get(base_video_url + id).text
    soup = BeautifulSoup(response, 'lxml')
    cover = soup.find('img', attrs=['class', 'hvpi-cover'])
    return cover['src']

def download(id: str) -> str:
    response = requests.get(base_video_url + id).text
    soup = BeautifulSoup(response, 'lxml')
    download = soup.find('a', attrs=['class', 'hvpab-btn flex align-center primary-color-hover'])
    return base_url + download['href']

def tags(id: str) -> list:
    response = requests.get(base_video_url + id).text
    soup = BeautifulSoup(response, 'lxml')
    tags = soup.find('div', attrs=['class', 'hvpis-text grey--text text--lighten-1']).findChildren("a")
    fulltags = []

    for tag in tags:
        fulltags.append(tag['href'].replace('/browse/tags/', ''))

    return fulltags
