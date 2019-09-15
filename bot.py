import discord
import apihandler
import anilist
import random

client = discord.Client()

@client.event
async def on_ready():
    print('Logged on as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!lookup'):
        searchTerm = message.content.split(' ', 1)[1]
        await lookup(searchTerm, message.channel)
    
    if message.content.startswith('!recommend'):
        animeId = message.content.split(' ', 2)[2]
        user = message.mentions

        helpMessage = 'Proper usage: `!recommend @user <id>`'
        if len(user) != 1:
            await message.channel.send(helpMessage)

        try:
            int(animeId)
        except TypeError:
            await message.channel.send(helpMessage + ' (<id> must be an int)')

        await recommend(user[0], animeId, message.channel)

    if message.content.startswith('!myrecommendations'):
        userId = message.author.id

        await getRecommendations(userId, message.channel)

    if message.content.startswith('!hello'):
        await message.channel.send('Please don\'t talk to me, {}, you filthy weeb.'.format(message.author.name))

#    for word in message.contet.split(''):
#        if word in weebWords:
#            await message.channel.send(random.choice(weebResponses))


async def lookup(term, channel):
    response = None
    try:
        response = apihandler.search(term)
    except Exception as e:
        await channel.send(e)
    
    if len(response) > 1:
        msg = 'Please select an anime by responding with its number:\n'
        n = 1
        for anime in response:
            msg += '{}: {} ({})\n'.format(n, anime['title'], anime['year'])
            n += 1

        botmsg = await channel.send(msg) 
        reply = await client.wait_for('message')

        try:
            await channel.delete_messages([reply, botmsg])
            animeId = response[int(reply.content) - 1]['id']
            anime = apihandler.getAnime(animeId)
            await channel.send(embed=anime.toEmbed())
        except Exception as e:
            await channel.send('error: {}'.format(e))
    else:
        await channel.send(embed=response[0].toEmbed())

async def recommend(user, animeId, channel):
    anime = None
    try:
        anime = apihandler.getAnime(animeId)
    except Exception as e:
        await channel.send(e)

    if not anime:
        await channel.send('No anime found with id ' + animeId)
    
    anime.userId = user.id

    try:
        apihandler.postRecommendation(anime)
        await channel.send('{} was recommended to {}'.format(anime.title if anime.title else anime.romaji, user.name))
    except Exception as e:
        await channel.send(e)

async def getRecommendations(userId, channel):
    recommendations = apihandler.getRecommendations(userId)

    embed = discord.Embed()
    recommendationList = ''

    for anime in recommendations:
        recommendationList += '{} - [AniList]({}) [MAL]({})\n'.format(
            anime.title if anime.title else anime.romaji,
            anime.anilistLink,
            anime.malLink
        )  

    embed.add_field(
        name='Recommendations:',
        value=recommendationList,
        inline=False
    )
    
    await channel.send(embed=embed)



if __name__ == '__main__':
    client.run('')