import discord
import praw
import asyncio
import random
client = discord.Client()
reddit = praw.Reddit(
    client_id = "G3TXu7-HWaZ19w",
    client_secret = "LCRX-tx2XLI3CnPmslzfrzWTuDr7Cw",
    password = "facileslopes",
    user_agent = "Top10s Game by u/knightlord6",
    username = "knightlord6",
)
def create_full_embed(names,lst):
    embed = discord.Embed(title="Your Top 10s!",description="The Top 10 Posts according to every player", color=0xffff00)
    for name in names:
        value='Your Top 10 Posts'
        for x in range(1,11):
            value = value + '\n' + '**'+str(x)+ '**. ' + lst[names.index(name)][x-1]
        embed.add_field(name=name,value=value,inline=True)
    return embed
@client.event
async def on_ready():
    print('Hello, I am {0.user}'.format(client))

@client.event
async def on_message(message):
    scores = []
    if message.author == client.user:
        return
    if message.content.startswith('$playgame'):
        await message.channel.send('What subreddit do you want to play today?')
        def Check(m):
            return m.content.startswith("$")
        Subreddit = await client.wait_for('message', check=Check)
        await message.channel.send('Over what time period do you want to sort by?(day,week,month,year,all)?')
        SortPeriod = await client.wait_for('message', check=Check)
        n = 1
        TopPost = []
        Error = False
        try:
            for submission in reddit.subreddit(Subreddit.content[1:]).top(SortPeriod.content[1:],limit=10):
                if submission.is_self:
                    TopPost.append([submission.title,submission.selftext,submission.is_self])
                else:
                    TopPost.append([submission.title,submission.url,submission.is_self])
                n += 1
        except:
            await message.channel.send('Either the entered subreddit does not exist, or the sorting period is incorrect')
            Error = True
        if Error == False:
            TopPosts = tuple(TopPost)
            ResortedPosts = list(TopPosts)
            random.shuffle(ResortedPosts)
            await message.channel.send("Who all will be playing this game?")
            list_of_players = await client.wait_for('message',check=Check)
            players = list_of_players.content[1:].split(',')
            ChosenSequences = []
            for player in players:
                ChosenSequences.append(["-" for x in range(1,11)])
            await message.channel.send(embed=create_full_embed(players,ChosenSequences))
            for Post in ResortedPosts:
                if Post[2] == False:
                    post_embed = discord.Embed(title = Post[0],description = Post[1],color=0x00ff00)
                    post_embed.set_image(url=Post[1])
                    await message.channel.send(embed=post_embed)
                else:
                    if len(Post[1]) < 2048:
                        post_embed = discord.Embed(title = Post[0],description = Post[1],color=0x00ff00)
                        await message.channel.send(embed=post_embed)
                    else:
                        post_embed = discord.Embed(title = Post[0],description = '',color=0x00ff00)
                        await message.channel.send(embed=post_embed)
                        for x in range(2000,len(Post[1]),2000):
                            await message.channel.send(Post[1][x-2000:x])                       
                for player in players:
                    await message.channel.send(player + ', what place do you think this post is at?')
                    a = await client.wait_for('message', check=Check)
                    ChosenSequences[players.index(player)][int(a.content[1:])-1] = Post[0]
                for player in players:
                    Edits = True
                    while Edits == True:
                        await message.channel.send(player +", do you want to make any edits(Y/N)?",embed=create_full_embed(players,ChosenSequences))
                        EditsMade = await client.wait_for('message', check=Check)
                        if EditsMade.content == "$Y":
                            await message.channel.send("Which post do you want to move?(Enter the number)")
                            move_from = await client.wait_for('message', check=Check)
                            await message.channel.send("Which place do you want to move it to?(Enter the number)")
                            destination = await client.wait_for('message', check=Check)
                            move_from_int = int(move_from.content[1:]) - 1
                            destination_int = int(destination.content[1:]) - 1
                            unassigned = ChosenSequences[players.index(player)][destination_int]
                            ChosenSequences[players.index(player)][destination_int] = ChosenSequences[players.index(player)][move_from_int]
                            ChosenSequences[players.index(player)][move_from_int] = '-'
                            while unassigned != '-':
                                await message.channel.send('The #' + str(destination_int + 1) + " post was displaced. Where do you want to move it now?")
                                destination = await client.wait_for('message', check=Check)
                                destination_int = int(destination.content[1:]) - 1
                                unassigned2 = ChosenSequences[players.index(player)][destination_int]
                                ChosenSequences[players.index(player)][destination_int] = unassigned
                                unassigned = unassigned2
                        else:
                            Edits = False
                await message.channel.send("Then let's move on!")
            for player in players:
                scores.append(0)
                for x in range(0,10):
                    if TopPosts[x][0] == ChosenSequences[players.index(player)][x]:
                        scores[players.index(player)] += 3
                        ChosenSequences[players.index(player)][x] += ' **CORRECT! - 3 pts**'
                    elif x == 0:
                        if TopPosts[x+1][0] == ChosenSequences[players.index(player)][x]:
                            scores[players.index(player)] += 1
                            ChosenSequences[players.index(player)][x] += ' **Slightly correct! - 1 pts**'
                        else:
                            scores[players.index(player)] += 0
                            ChosenSequences[players.index(player)][x] += ' **Wrong - 0 pts**'
                    elif x == 9:
                        if TopPosts[x-1][0] == ChosenSequences[players.index(player)][x]:
                            scores[players.index(player)] += 1
                            ChosenSequences[players.index(player)][x] += ' **Slightly correct! - 1 pts**'
                        else:
                            scores[players.index(player)] += 0
                            ChosenSequences[players.index(player)][x] += ' **Wrong - 0 pts**'
                    elif TopPosts[x-1][0] == ChosenSequences[players.index(player)][x] or TopPosts[x+1][0] == ChosenSequences[players.index(player)][x]:
                        scores[players.index(player)] += 1
                        ChosenSequences[players.index(player)][x] += ' **Slightly correct! - 1 pts**'
                    else:
                        scores[players.index(player)] += 0
                        ChosenSequences[players.index(player)][x] += ' **Wrong - 0 pts**'
            print(ChosenSequences)
            TopPostsEmbed = discord.Embed(title= "Top Posts of r/" + Subreddit.content[1:],description="The Top 10 Posts of this subreddit", color=0x00ff00)
            for x in range(1,11):
                TopPostsEmbed.add_field(name= str(x)+".", value=TopPosts[x-1][0],inline=False)
            await message.channel.send("Here is the actual Top 10 posts",embed=TopPostsEmbed)
            await message.channel.send("Here is each player's Top 10 list!")
            for x in range(0,len(players)):
                PlayerEmbed = discord.Embed(title=players[x] + "'s Top 10!",description = '',color=0x00ff00)
                for y in range(1,11):
                    PlayerEmbed.add_field(name= str(y)+".", value=ChosenSequences[x][y-1],inline=False)
                await message.channel.send(embed=PlayerEmbed)
            score_tuple = tuple(scores)
            scores.sort(reverse=True)
            ScoreEmbed = discord.Embed(title='Player Scores',description = '',color=0x00ff00)
            for x in range (0,len(players)):
                print(players[score_tuple.index(scores[x])])
                ScoreEmbed.add_field(name=str(x+1) + '. ',value = players[score_tuple.index(scores[x])] + " - " + str(scores[x]))
            await message.channel.send("Here is everyone's scores!",embed=ScoreEmbed)
    if message.content.startswith('$info'):
        InfoEmbed = discord.Embed(title= 'The Top10sGame Bot!',description="", color=0x00ff00)
        InfoEmbed.add_field(name='What is this bot about?', value='Programmed in Python, this bot allows you to play a game where you attempt to guess the top 10 posts of a subreddit of your choice. Can be played by one or multiple people.')
        InfoEmbed.add_field(name='How do I play?',value='Start a game with $playgame! The bot will prompt you, and you can answer to it with the $ prefix!')
        await message.channel.send(embed=InfoEmbed)
    if message.content.startswith('$amogus'):
        await message.channel.send('When the impostor is sus!')
        await message.channel.send('⡯⡯⡾⠝⠘⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢊⠘⡮⣣⠪⠢⡑⡌ ⠀⠀⠀⠟⠝⠈⠀⠀⠀⠡⠀⠠⢈⠠⢐⢠⢂⢔⣐⢄⡂⢔⠀⡁⢉⠸⢨⢑⠕⡌ ⠀⠀⡀⠁⠀⠀⠀⡀⢂⠡⠈⡔⣕⢮⣳⢯⣿⣻⣟⣯⣯⢷⣫⣆⡂⠀⠀⢐⠑⡌ ⢀⠠⠐⠈⠀⢀⢂⠢⡂⠕⡁⣝⢮⣳⢽⡽⣾⣻⣿⣯⡯⣟⣞⢾⢜⢆⠀⡀⠀⠪ ⣬⠂⠀⠀⢀⢂⢪⠨⢂⠥⣺⡪⣗⢗⣽⢽⡯⣿⣽⣷⢿⡽⡾⡽⣝⢎⠀⠀⠀⢡ ⣿⠀⠀⠀⢂⠢⢂⢥⢱⡹⣪⢞⡵⣻⡪⡯⡯⣟⡾⣿⣻⡽⣯⡻⣪⠧⠑⠀⠁⢐ ⣿⠀⠀⠀⠢⢑⠠⠑⠕⡝⡎⡗⡝⡎⣞⢽⡹⣕⢯⢻⠹⡹⢚⠝⡷⡽⡨⠀⠀⢔ ⣿⡯⠀⢈⠈⢄⠂⠂⠐⠀⠌⠠⢑⠱⡱⡱⡑⢔⠁⠀⡀⠐⠐⠐⡡⡹⣪⠀⠀⢘ ⣿⣽⠀⡀⡊⠀⠐⠨⠈⡁⠂⢈⠠⡱⡽⣷⡑⠁⠠⠑⠀⢉⢇⣤⢘⣪⢽⠀⢌⢎ ⣿⢾⠀⢌⠌⠀⡁⠢⠂⠐⡀⠀⢀⢳⢽⣽⡺⣨⢄⣑⢉⢃⢭⡲⣕⡭⣹⠠⢐⢗ ⣿⡗⠀⠢⠡⡱⡸⣔⢵⢱⢸⠈⠀⡪⣳⣳⢹⢜⡵⣱⢱⡱⣳⡹⣵⣻⢔⢅⢬⡷ ⣷⡇⡂⠡⡑⢕⢕⠕⡑⠡⢂⢊⢐⢕⡝⡮⡧⡳⣝⢴⡐⣁⠃⡫⡒⣕⢏⡮⣷⡟ ⣷⣻⣅⠑⢌⠢⠁⢐⠠⠑⡐⠐⠌⡪⠮⡫⠪⡪⡪⣺⢸⠰⠡⠠⠐⢱⠨⡪⡪⡰ ⣯⢷⣟⣇⡂⡂⡌⡀⠀⠁⡂⠅⠂⠀⡑⡄⢇⠇⢝⡨⡠⡁⢐⠠⢀⢪⡐⡜⡪⡊ ⣿⢽⡾⢹⡄⠕⡅⢇⠂⠑⣴⡬⣬⣬⣆⢮⣦⣷⣵⣷⡗⢃⢮⠱⡸⢰⢱⢸⢨⢌ ⣯⢯⣟⠸⣳⡅⠜⠔⡌⡐⠈⠻⠟⣿⢿⣿⣿⠿⡻⣃⠢⣱⡳⡱⡩⢢⠣⡃⠢⠁ ⡯⣟⣞⡇⡿⣽⡪⡘⡰⠨⢐⢀⠢⢢⢄⢤⣰⠼⡾⢕⢕⡵⣝⠎⢌⢪⠪⡘⡌⠀ ⡯⣳⠯⠚⢊⠡⡂⢂⠨⠊⠔⡑⠬⡸⣘⢬⢪⣪⡺⡼⣕⢯⢞⢕⢝⠎⢻⢼⣀⠀ ⠁⡂⠔⡁⡢⠣⢀⠢⠀⠅⠱⡐⡱⡘⡔⡕⡕⣲⡹⣎⡮⡏⡑⢜⢼⡱⢩⣗⣯⣟ ⢀⢂⢑⠀⡂⡃⠅⠊⢄⢑⠠⠑⢕⢕⢝⢮⢺⢕⢟⢮⢊⢢⢱⢄⠃⣇⣞⢞⣞⢾ ⢀⠢⡑⡀⢂⢊⠠⠁⡂⡐⠀⠅⡈⠪⠪⠪⠣⠫⠑⡁⢔⠕⣜⣜⢦⡰⡎⡯⡾⡽⡯⡯⡾⠝⠘⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢊⠘⡮⣣⠪⠢⡑⡌ ⠀⠀⠀⠟⠝⠈⠀⠀⠀⠡⠀⠠⢈⠠⢐⢠⢂⢔⣐⢄⡂⢔⠀⡁⢉⠸⢨⢑⠕⡌ ⠀⠀⡀⠁⠀⠀⠀⡀⢂⠡⠈⡔⣕⢮⣳⢯⣿⣻⣟⣯⣯⢷⣫⣆⡂⠀⠀⢐⠑⡌ ⢀⠠⠐⠈⠀⢀⢂⠢⡂⠕⡁⣝⢮⣳⢽⡽⣾⣻⣿⣯⡯⣟⣞⢾⢜⢆⠀⡀⠀⠪ ⣬⠂⠀⠀⢀⢂⢪⠨⢂⠥⣺⡪⣗⢗⣽⢽⡯⣿⣽⣷⢿⡽⡾⡽⣝⢎⠀⠀⠀⢡ ⣿⠀⠀⠀⢂⠢⢂⢥⢱⡹⣪⢞⡵⣻⡪⡯⡯⣟⡾⣿⣻⡽⣯⡻⣪⠧⠑⠀⠁⢐ ⣿⠀⠀⠀⠢⢑⠠⠑⠕⡝⡎⡗⡝⡎⣞⢽⡹⣕⢯⢻⠹⡹⢚⠝⡷⡽⡨⠀⠀⢔ ⣿⡯⠀⢈⠈⢄⠂⠂⠐⠀⠌⠠⢑⠱⡱⡱⡑⢔⠁⠀⡀⠐⠐⠐⡡⡹⣪⠀⠀⢘ ⣿⣽⠀⡀⡊⠀⠐⠨⠈⡁⠂⢈⠠⡱⡽⣷⡑⠁⠠⠑⠀⢉⢇⣤⢘⣪⢽⠀⢌⢎ ⣿⢾⠀⢌⠌⠀⡁⠢⠂⠐⡀⠀⢀⢳⢽⣽⡺⣨⢄⣑⢉⢃⢭⡲⣕⡭⣹⠠⢐⢗ ⣿⡗⠀⠢⠡⡱⡸⣔⢵⢱⢸⠈⠀⡪⣳⣳⢹⢜⡵⣱⢱⡱⣳⡹⣵⣻⢔⢅⢬⡷ ⣷⡇⡂⠡⡑⢕⢕⠕⡑⠡⢂⢊⢐⢕⡝⡮⡧⡳⣝⢴⡐⣁⠃⡫⡒⣕⢏⡮⣷⡟ ⣷⣻⣅⠑⢌⠢⠁⢐⠠⠑⡐⠐⠌⡪⠮⡫⠪⡪⡪⣺⢸⠰⠡⠠⠐⢱⠨⡪⡪⡰ ⣯⢷⣟⣇⡂⡂⡌⡀⠀⠁⡂⠅⠂⠀⡑⡄⢇⠇⢝⡨⡠⡁⢐⠠⢀⢪⡐⡜⡪⡊ ⣿⢽⡾⢹⡄⠕⡅⢇⠂⠑⣴⡬⣬⣬⣆⢮⣦⣷⣵⣷⡗⢃⢮⠱⡸⢰⢱⢸⢨⢌ ⣯⢯⣟⠸⣳⡅⠜⠔⡌⡐⠈⠻⠟⣿⢿⣿⣿⠿⡻⣃⠢⣱⡳⡱⡩⢢⠣⡃⠢⠁ ⡯⣟⣞⡇⡿⣽⡪⡘⡰⠨⢐⢀⠢⢢⢄⢤⣰⠼⡾⢕⢕⡵⣝⠎⢌⢪⠪⡘⡌⠀ ⡯⣳⠯⠚⢊⠡⡂⢂⠨⠊⠔⡑⠬⡸⣘⢬⢪⣪⡺⡼⣕⢯⢞⢕⢝⠎⢻⢼⣀⠀ ⠁⡂⠔⡁⡢⠣⢀⠢⠀⠅⠱⡐⡱⡘⡔⡕⡕⣲⡹⣎⡮⡏⡑⢜⢼⡱⢩⣗⣯⣟ ⢀⢂⢑⠀⡂⡃⠅⠊⢄⢑⠠⠑⢕⢕⢝⢮⢺⢕⢟⢮⢊⢢⢱⢄⠃⣇⣞⢞⣞⢾ ⢀⠢⡑⡀⢂⢊⠠⠁⡂⡐⠀⠅⡈⠪⠪⠪⠣⠫⠑⡁⢔⠕⣜⣜⢦⡰⡎⡯⡾⡽')
client.run('ODM5NDE1NzAxOTI0MzQ3OTU2.YJJUyg.hEwvcDkJIQU3lqIYFbW8GbzsHTU')
