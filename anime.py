from discord import Embed
class Anime():
    def __init__(self, title, english, romaji, japanese, description, rating, image):
        self.title = title
        self.englishTitle = english
        self.romajiTitle = romaji 
        self.japaneseTitle = japanese
        self.description = description
        self.rating = rating
        self.image = image
    
    def toEmbed(self):
        embed = Embed()

        embed.title = self.title
        embed.set_image(
                url=self.image
            ).add_field(
                name='Alternate Titles:',
                value=altTitlesToString(self.englishTitle, self.romajiTitle, self.japaneseTitle),
                inline=False
            ).add_field(
                name='Score:',
                value=self.rating,
                inline=False
            )
        
        return embed

def altTitlesToString(e, r, j):
    s = ''
    if e:
        s += e + '\n'
    if r:
        s += r + '\n'
    if j:
        s += j + '\n'
    
    return s
    
    
