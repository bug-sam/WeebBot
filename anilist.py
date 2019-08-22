import requests

req = requests.Session()

url = 'https://graphql.anilist.co'

search_query = '''query ($search: String) {
    Media(search: $search) {
      id
      idMal
    }
}'''

def getLinks(title):
    search_variables = {
        'search': title
    }

    payload = {
        'query': search_query,
        'variables': search_variables
    }

    response = req.post(url, json=payload).json()
    req.close()

    data = response['data']['Media']

    return {
        'anilistUrl': 'https://anilist.co/anime/' + str(data['id']), 
        'malUrl': 'https://myanimelist.net/anime/' + str(data['idMal'])
    }