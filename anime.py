from discord import Embed

class Anime:
    def __init__(self, title, romaji, native, description, score, anilistLink, malLink, image, userId=None):
        self.title = title
        self.romaji = romaji
        self.native = native
        self.description = description
        self.score = score
        self.anilistLink = anilistLink
        self.malLink = malLink
        self.image = image
        self.userId = userId

    def toEmbed(self):
        embed = Embed()
        if self.title:
            embed.title = self.title
            altTitles = self.romaji + '\n' + self.native
        else:
            embed.title = self.romaji
            altTitles = self.native

        embed.set_image(
                url=self.image
            ).add_field(
                name='Alternate Titles:',
                value=altTitles,
                inline=False
            ).add_field(
                name='Score:',
                value=str(self.score),
                inline=False
            ).add_field(
                name='Links',
                value='[AniList]({}) [MAL]({})'.format(self.anilistLink, self.malLink)
            )
        
        return embed

    def toDict(self):
        dictionary = {
            'title': self.title,
            'japaneseTitles': {
                'romaji': self.romaji,
                'native': self.native
            },
            'description': self.description,
            'score': self.score,
            'links': {
                'anilist': self.anilistLink,
                'mal': self.malLink
            },
            'image': self.image
        }
        
        if self.userId:
            dictionary['userId'] = self.userId
        
        return dictionary