import requests
from bs4 import BeautifulSoup
import codecs

website = 'https://www.tamilpaa.com/tamil-movies-list'
response = requests.get(website)
content = response.content
soup = BeautifulSoup(content)
detail_content = soup.find('table', attrs={'class': 'standard mb-50px'})
tablecontent = detail_content.find_all('tr')

list_of_movies = []

for tr in tablecontent[1:]:
    song = {}
    a_tags = tr.find_all('a')
    td_tags = tr.find_all('td')

    song["movie_url"] = a_tags[0].get('href')
    song["வருடம்"] = td_tags[1].get_text()
    song["இசையமைப்பாளர்"] = td_tags[2].get_text()
    list_of_movies.append(song)


songs_data = []


def crawl_movie_url(movie):
    response = requests.get(movie["movie_url"])
    content = response.content
    soup = BeautifulSoup(content)

    detail_content = soup.find('table', attrs={'class': 'standard'})

    td_tags = detail_content.find_all('td')
    movie["திரைப்படம்"] = td_tags[2].get_text()

    song_div = soup.find('div', attrs={'class': 'tab-content clearfix', 'id': 'tab_1'})
    song_li_tags = song_div.find_all('li')

    for song_li in song_li_tags:
        song = {}
        song["திரைப்படம்"] = movie["திரைப்படம்"]
        s = song_li.find('a').get_text().split('(')
        song["பாடல்_பெயர்"] = s[1][:-3].strip('\n')
        song["இசையமைப்பாளர்"] = movie["இசையமைப்பாளர்"]
        song["வருடம்"] = movie["வருடம்"]
        songs_data.append(song)


for movie in list_of_movies:
    crawl_movie_url(movie)

final_corpus = []


def crawl_song_url(song):
    response = requests.get(song["song_url"])
    content = response.content
    soup = BeautifulSoup(content)
    detail_content = soup.find('table', attrs={'class': 'standard mb-10px'})
    tablecontent = detail_content.find_all('td')
    song["பாடியவர்கள்"] = tablecontent[4].get_text()

    song_content = soup.find('div', attrs={'class': 'info-box white-bg'})

    song["பாடல்வரிகள்"] = (song_content.get_text()).strip()
    del song["song_url"]
    final_corpus.append(song)


for song in songs_data:
    try:
        crawl_song_url(song)
    except Exception as e:
        print(e)

f = codecs.open('scraped_text.txt', 'w', encoding='utf-8')
for line in final_corpus:
    try:
        song_json = str(line).replace("\'", "\"")
        f.write(song_json)
        f.write('\n')
    except Exception as e:
        print(e)
