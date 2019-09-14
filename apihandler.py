import requests
from anime import Anime

session = requests.Session()
session.headers = {
    'Accept': 'application/vnd.api+json',
    'Content-Type': 'application/vnd.api+json'
}

def search(title):
    url = 'https://stateless.pythonanywhere.com/anilist/search?title=' + title.replace(' ', '%20')

    response = session.get(url, timeout=4)
    response.raise_for_status

    return response.json()['anime']


def getAnime(animeId):
    url = 'https://stateless.pythonanywhere.com/anilist/anime?id=' + str(animeId)

    response = session.get(url, timeout=4)
    response.raise_for_status
    animejson = response.json()['anime']

    anime = Anime(
        animejson['title'],
        animejson['japaneseTitles']['romaji'],
        animejson['japaneseTitles']['native'],
        animejson['description'],
        animejson['score'],
        animejson['links']['anilist'],
        animejson['links']['mal'],
        animejson['image']
    )

    return anime