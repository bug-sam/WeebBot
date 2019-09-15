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

    if animejson:
        anime = Anime(
            animejson['title'],
            animejson['japaneseTitles']['romaji'],
            animejson['japaneseTitles']['native'],
            animejson['description'],
            animejson['score'],
            animejson['links']['anilist'],
            animejson['links']['mal'],
            animejson['image'],
            animeId
        )

        return anime
    
    return None

def postRecommendation(anime):
    url = 'https://stateless.pythonanywhere.com/animewebapi/recommendations'

    response = session.post(url, json=anime.toDict())
    response.raise_for_status

def getRecommendations(userId):
    url = 'https://stateless.pythonanywhere.com/animewebapi/recommendations?userId=' + str(userId)

    response = session.get(url)
    response.raise_for_status
    
    anime = []
    animejson = response.json()['anime']

    for a in animejson:
        anime.append(Anime(
            a['title'],
            a['japaneseTitles']['romaji'],
            a['japaneseTitles']['native'],
            a['description'],
            a['score'],
            a['links']['anilist'],
            a['links']['mal'],
            a['image']
        ))

    return anime
    