import requests
from difflib import SequenceMatcher
from anime import Anime

session = requests.Session()
session.headers = {
    'Accept': 'application/vnd.api+json',
    'Content-Type': 'application/vnd.api+json'
}

def searchForAnime(title):
    url = 'https://kitsu.io/api/edge/anime?filter[text]=' + title.replace(' ', '%20')

    response = session.get(url, timeout=4)
    response.raise_for_status()
    return parse(response.json()['data'])

def parse(response):
    parsed = []

    for anime in response:
        title = anime['attributes']['canonicalTitle']

        title_romaji = get_title_by_language_codes(
            anime['attributes']['titles'],
            ['en_jp']
        )
        title_english = get_title_by_language_codes(
            anime['attributes']['titles'],
            ['en', 'en_us']
        )
        title_japanese = get_title_by_language_codes(
            anime['attributes']['titles'],
            ['ja_jp']
        )

        rating = anime['attributes']['averageRating']

        description = anime['attributes']['synopsis']

        image = anime['attributes']['posterImage']['tiny']

        parsed.append(Anime(
            title,
            title_english,
            title_japanese, 
            title_romaji,
            description,
            rating,
            image
        ))

    return parsed


def get_title_by_language_codes(titles, codes):
    for language_code in codes:
        if language_code in titles:
            return titles[language_code]
    return None

def getClosest(response, title):
    closeness = {}
    for anime in response:
        if anime['title']:
            if anime['title'].lower() == title.lower() or title.lower() in anime['title'].lower():
                return anime
            closeness[SequenceMatcher(None, anime['title'], title).ratio()] = anime
    
    return closeness[min(closeness.keys())]