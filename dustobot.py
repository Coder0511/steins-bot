import random
import help
import asyncio
import discord
import typing
import wavelink
import paints
import videos
import nekos
import spotipy
import requests
import pandas
from spotipy.oauth2 import SpotifyClientCredentials
from discord.ext import commands
from itertools import islice
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
	    if isinstance(error, commands.CommandOnCooldown):
		    return await ctx.send(embed=discord.Embed(title="Yo hold up, there's a cooldown of 10 seconds for this command ({} remaining)".format(round(error.retry_after, 2)), color=discord.Color.from_rgb(255, 255, 255)))
    
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Command for syncing commands on runtime

"""class Sync(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="sync", aliases=["Sync"])
    @commands.is_owner()
    async def sync_command(self, ctx: commands.Context):
        await ctx.bot.tree.sync()
        print("Synced")
    
    @commands.command(name="reload", aliases=["Reload"])
    @commands.is_owner()
    async def reload_command(self, *, module : str):
        self.bot.unload_extension(module)
        self.bot.load_extension(module)"""    

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class DumbCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="ping", aliases=["Ping"])
    async def ping_command(self, ctx: commands.Context):
        await ctx.send(embed=discord.Embed(title="Pong", color=discord.Color.from_rgb(255, 255, 255))) 

    @commands.command(name="CoinFlip", aliases=["cf", "coinflip", "Cf", "CF", "cF", "Coinflip", "coinFlip"])
    async def coin_flip(self, ctx: commands.Context):
        flip = random.randint(0, 1)
        if flip==0:
            return await ctx.reply(embed=discord.Embed(title="Behold!! A coin flip\nHeads", color=discord.Color.from_rgb(255, 255, 255)))
        else:
            return await ctx.reply(embed=discord.Embed(title="Behold!! A coin flip\nTails", color=discord.Color.from_rgb(255, 255, 255)))
    
    @commands.command(name="DiceRoll", aliases=["dice", "diceroll", "dr", "Dice", "Dr", "diceRoll", "Diceroll", "dR", "DR"])
    async def dice_roll(self, ctx: commands.Context):
        dice = random.randint(1, 6)
        return await ctx.reply(embed=discord.Embed(title="You got a {}".format(dice), color=discord.Color.from_rgb(255, 255, 255)))

    @commands.command(name="RandomNumber", aliases=["randomnumber", "rn", "RN", "rN", "Rn", "Randomnumber", "randomNumber"])
    async def random_number(self, ctx:commands.Context, number1: str=None, number2: str=None):
        if number1==None or number2==None:
             return await ctx.reply(embed=discord.Embed(title="Please enter two valid numbers next to the command", color=discord.Color.from_rgb(255, 255, 255)))
        
        try:
            if int(number1) > int(number2):
                return await ctx.reply(embed=discord.Embed(title="First number should be lower than the second one", color=discord.Color.from_rgb(255, 255, 255)))
            elif int(number1) == int(number2):
                return await ctx.reply(embed=discord.Embed(title="I could generate a number between {} and {}, but the result won't change at all...".format(number1, number2), color=discord.Color.from_rgb(255, 255, 255)))
            
            random_num = random.randint(int(number1), int(number2))
            return await ctx.reply(embed=discord.Embed(title="Random number: {}".format(random_num), color=discord.Color.from_rgb(255, 255, 255)))
        except:
            return await ctx.reply(embed=discord.Embed(title="Whoops, looks like something went wrong.\nPlease write two numbers without decimals to generate a random number", color=discord.Color.from_rgb(255, 255, 255)))

    @commands.command(aliases=["rps", "RPS", "Rps"])
    async def rock_paper_scissors(self, ctx:commands.Context, choice: str=""):
        response = ""
        machine = ""
        machine_number = random.randint(1, 3)
        
        if machine_number == 1:
            machine = "rock"
        elif machine_number == 2:
            machine = "paper"
        else:
            machine = "scissors"

        choice = choice.lower()

        if (choice == "rock") or (choice == "paper") or (choice == "scissors"):
            if machine == choice:
                response ="It's a tie"
            elif (choice == "rock") and (machine == "scissors"):
                response ="You won against scissors {}".format(":scissors:")
            elif (choice == "rock") and (machine == "paper"):
                response ="You lost against paper {}".format(":roll_of_paper:")
            elif (choice == "paper") and (machine == "rock"):
                response ="You won against rock {}".format(":rock:")
            elif (choice == "paper") and (machine == "scissors"):
                response ="You lost against scissors {}".format(":scissors:")
            elif (choice == "scissors") and (machine == "paper"):
                response ="You won against paper {}".format(":roll_of_paper:")
            elif (choice == "scissors") and (machine == "rock"):
                response ="You lost against rock {}".format(":rock:")
        else:
            response ="Whoops, looks like you inserted your choice incorrectly. Please try again with 'rock', 'paper' or 'scissors'"
        
        return await ctx.reply(embed=discord.Embed(title=response, color=discord.Color.from_rgb(255, 255, 255)))

    @commands.command(aliases=["sauce", "Sauce"])
    async def sauce_command(self, ctx:commands.Context):
        number = random.randint(1, 462630)
        return await ctx.send(embed=discord.Embed(title=number, color=discord.Color.from_rgb(255, 255, 255)))
    
    @commands.command(aliases=["urban", "Urban", "ud", "UD", "Ud", "uD", "urbandictionary", "UrbanDictionary", "urbanDictionary"])
    @commands.cooldown(1, 10, commands.BucketType.channel)
    async def urban_command(self, ctx:commands.Context, *, search: str=""):
        try:
            if search=="":
                return await ctx.send(embed=discord.Embed(title="Type any term to search it on Urban Dictionary", color=discord.Color.from_rgb(255, 255, 255)))   

            response = requests.get(f"http://api.urbandictionary.com/v0/define?term={search}")
            search = response.json()
            search = search["list"]

            if len(search) == 0:
                return await ctx.send(embed=discord.Embed(title="Whoops, looks like I couldn't find the term you were loking for :(", color=discord.Color.from_rgb(255, 255, 255)))  

            search = search[0]

            definition = search["definition"]
            definition = definition.replace("[", "").replace("]", "")

            example = search["example"]
            example = example.replace("[", "").replace("]", "")

            if (len(definition) > 2000) or (len(example) > 2000):
                answer = search["permalink"]
                return await ctx.send(embed=discord.Embed(description=answer, color=discord.Color.from_rgb(255, 255, 255)))  

            title = search["word"]
            title = title.replace("[", "").replace("]", "")

            author = search["author"]
            author = author.replace("[", "").replace("]", "")

            date = search["written_on"][0:10]
            date = date.replace("-", "")
            date_format = pandas.to_datetime(date)
            year = date_format.year
            month = date_format.month_name()
            day = date_format.day
            
            my_embed = discord.Embed(title="Urban Dictionary", color=discord.Color.from_rgb(255, 255, 255))
            my_embed.add_field(name="Word", value=title, inline=False)
            my_embed.add_field(name="", value="")
            my_embed.add_field(name="Definition", value=definition, inline=False)
            my_embed.add_field(name="", value="")
            my_embed.add_field(name="Example", value=example, inline=False)
            my_embed.add_field(name="", value="")
            my_embed.add_field(name="By {} {} {}, {}".format(author, month, day, year), value="", inline=False)
            
            return await ctx.send(embed=my_embed)
        except:
            print("Error found on Urban Dictionary Command")  
        
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.position = 0
        self.repeat = False
        self.repeatMode = "NONE"
        self.playingTextChannel = 0
        self.sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id="ae86a2b160874edf9dbb6b69995b74a8", client_secret="d470e67805824350b4c778554ed89a12"))
        self.looping_track = False
        self.looping_queue = False
        self.looped_track = ""
        self.queue_index_in_loop = 0
        bot.loop.create_task(self.create_nodes())
    
    async def create_nodes(self):
        await self.bot.wait_until_ready()
        
        node: wavelink.Node = wavelink.Node(uri='http://127.0.0.1:2333', password='youshallnotpass')
        await wavelink.NodePool.connect(client=self.bot, nodes=[node])

    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Music Cog is now ready!")

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f"Node <{node.id}> is now Ready!")

    @commands.Cog.listener()
    async def on_wavelink_track_start(self, track: wavelink.YouTubeTrack):
        if self.looping_queue==False and self.looping_track==False:
            try:
                self.queue.pop(0)
            except:
                pass

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, payload=wavelink.TrackEventPayload):
        if str(payload.reason)=="FINISHED":
            if self.looping_track == True:
                channel = self.bot.get_channel(self.playingTextChannel)
                try:
                    await payload.player.play(self.looped_track)
                except:
                    return await channel.send(embed=discord.Embed(title=f"Something went wrong while playing **{next_track[0].title}**", color=discord.Color.from_rgb(255, 255, 255)))
                    
                return await channel.send(embed=discord.Embed(title=f"Now playing: {self.looped_track.title}", color=discord.Color.from_rgb(255, 255, 255)))

            elif self.looping_queue == True:
                if isinstance(self.queue[self.queue_index_in_loop], str):
                    next_track = await wavelink.YouTubeTrack.search(self.queue[self.queue_index_in_loop])
                elif isinstance(self.queue[self.queue_index_in_loop], wavelink.YouTubeMusicTrack):
                    next_track: wavelink.YouTubeMusicTrack = [self.queue[self.queue_index_in_loop]]
                else:
                    next_track: wavelink.YouTubeTrack = [self.queue[self.queue_index_in_loop]]
                            
                channel = self.bot.get_channel(self.playingTextChannel)

                try:
                    await payload.player.play(next_track[0])
                except:
                    if self.queue_index_in_loop == (len(self.queue)-1):
                        self.queue_index_in_loop = 0
                    else:
                        self.queue_index_in_loop += 1
                    return await channel.send(embed=discord.Embed(title=f"Something went wrong while playing **{next_track[0].title}**", color=discord.Color.from_rgb(255, 255, 255)))
                
                if self.queue_index_in_loop == (len(self.queue)-1):
                    self.queue_index_in_loop = 0
                else:
                    self.queue_index_in_loop += 1
                return await channel.send(embed=discord.Embed(title=f"Now playing: {next_track[0].title}", color=discord.Color.from_rgb(255, 255, 255)))

            else:
                self.looping_track = False
                self.looping_queue = False
                self.looped_track = ""
                self.queue_index_in_loop = 0

                if not len(self.queue) == 0:
                    if isinstance(self.queue[0], str):
                        next_track = await wavelink.YouTubeTrack.search(self.queue[0])
                    elif isinstance(self.queue[0], wavelink.YouTubeMusicTrack):
                        next_track: wavelink.YouTubeMusicTrack = [self.queue[0]]
                    else:
                        next_track: wavelink.YouTubeTrack = [self.queue[0]]
                            
                    channel = self.bot.get_channel(self.playingTextChannel)

                    try:
                        await payload.player.play(next_track[0])
                    except:
                        return await channel.send(embed=discord.Embed(title=f"Something went wrong while playing **{next_track[0].title}**", color=discord.Color.from_rgb(255, 255, 255)))
                        
                    await channel.send(embed=discord.Embed(title=f"Now playing: {next_track[0].title}", color=discord.Color.from_rgb(255, 255, 255)))
                else:
                    channel = self.bot.get_channel(self.playingTextChannel)
                    await channel.send(embed=discord.Embed(title="Playlist's over\nDisconnected", color=discord.Color.from_rgb(255, 255, 255)))
                    self.playingTextChannel = -1
                    return await payload.player.disconnect()
                
        elif str(payload.reason)=="LOAD_FAILED":
            if self.looping_track == True:
                self.looping_track = False
                self.looping_queue = False
                self.looped_track = ""
                self.queue_index_in_loop = 0

                print(payload.reason)
                if not len(self.queue) == 0:
                    if isinstance(self.queue[0], str):
                        next_track = await wavelink.YouTubeTrack.search(self.queue[0])
                    elif isinstance(self.queue[0], wavelink.YouTubeMusicTrack):
                        next_track: wavelink.YouTubeMusicTrack = [self.queue[0]]
                    else:
                        next_track: wavelink.YouTubeTrack = [self.queue[0]]
                            
                    channel = self.bot.get_channel(self.playingTextChannel)

                    try:
                        await payload.player.play(next_track[0])
                    except:
                        return await channel.send(embed=discord.Embed(title=f"Something went wrong while playing **{next_track[0].title}**", color=discord.Color.from_rgb(255, 255, 255)))
                    
                    await channel.send(embed=discord.Embed(title=f"Something went wrong when playing the track provided. Getting out of the loop\n\nNow playing: {next_track[0].title}", color=discord.Color.from_rgb(255, 255, 255)))
                else:
                    channel = self.bot.get_channel(self.playingTextChannel)
                    await channel.send(embed=discord.Embed(title="Playlist's over\nDisconnected", color=discord.Color.from_rgb(255, 255, 255)))
                    self.playingTextChannel = -1
                    return await payload.player.disconnect()

            elif self.looping_queue == True:
                if isinstance(self.queue[self.queue_index_in_loop], str):
                    next_track = await wavelink.YouTubeTrack.search(self.queue[self.queue_index_in_loop])
                elif isinstance(self.queue[self.queue_index_in_loop], wavelink.YouTubeMusicTrack):
                    next_track: wavelink.YouTubeMusicTrack = [self.queue[self.queue_index_in_loop]]
                else:
                    next_track: wavelink.YouTubeTrack = [self.queue[self.queue_index_in_loop]]
                            
                channel = self.bot.get_channel(self.playingTextChannel)

                try:
                    await payload.player.play(next_track[0])
                except:
                    if self.queue_index_in_loop == (len(self.queue)-1):
                        self.queue_index_in_loop = 0
                    else:
                        self.queue_index_in_loop += 1
                    return await channel.send(embed=discord.Embed(title=f"Something went wrong while playing **{next_track[0].title}**", color=discord.Color.from_rgb(255, 255, 255)))

                if self.queue_index_in_loop == (len(self.queue)-1):
                    self.queue_index_in_loop = 0
                else:
                    self.queue_index_in_loop += 1 
                return await channel.send(embed=discord.Embed(title=f"Something went wrong when playing the track provided. Playing next song in the looped queue\n\nNow playing: {next_track[0].title}", color=discord.Color.from_rgb(255, 255, 255)))
            
            else:
                self.looping_track = False
                self.looping_queue = False
                self.looped_track = ""
                self.queue_index_in_loop = 0

                print(payload.reason)
                if not len(self.queue) == 0:
                    if isinstance(self.queue[0], str):
                        next_track = await wavelink.YouTubeTrack.search(self.queue[0])
                    elif isinstance(self.queue[0], wavelink.YouTubeMusicTrack):
                        next_track: wavelink.YouTubeMusicTrack = self.queue[0]
                    else:
                        next_track: wavelink.YouTubeTrack = self.queue[0]
                            
                    channel = self.bot.get_channel(self.playingTextChannel)

                    try:
                        await payload.player.play(next_track[0])
                    except:
                        return await channel.send(embed=discord.Embed(title=f"Something went wrong while playing **{next_track[0].title}**", color=discord.Color.from_rgb(255, 255, 255)))
                    
                    await channel.send(embed=discord.Embed(title=f"Something went wrong when playing the track provided. Playing next song in the queue\n\nNow playing: {next_track[0].title}", color=discord.Color.from_rgb(255, 255, 255)))
                else:
                    channel = self.bot.get_channel(self.playingTextChannel)
                    await channel.send(embed=discord.Embed(title="Playlist's over\nDisconnected", color=discord.Color.from_rgb(255, 255, 255)))
                    self.playingTextChannel = -1
                    return await payload.player.disconnect()
            
        else:
            print(payload.reason)

    def get_playlist_tracks(self, the_playlist_id):
        temporal_tracks_list = []
        results = self.sp.playlist_items(the_playlist_id)
        tracks = results['items']
        while results['next']:
            results = self.sp.next(results)
            tracks.extend(results['items'])
        for i in tracks:
            temporal_tracks_list.append("{} - {}".format(i["track"]["name"], i["track"]["artists"][0]["name"]))
        return temporal_tracks_list

    def get_album_tracks(self, the_album_id):
        temporal_tracks_list = []
        results = self.sp.album_tracks(the_album_id)
        tracks = results['items']
        while results['next']:
            results = self.sp.next(results)
            tracks.extend(results['items'])
        for i in tracks:
            temporal_tracks_list.append("{} - {}".format(i["name"], i["artists"][0]["name"]))
        return temporal_tracks_list

    def get_the_track(self, the_track_id):
        result = self.sp.track(the_track_id)
        return "{} - {}".format(result["name"], result["artists"][0]["name"])
    
    @commands.command(name="join", aliases=["connect", "Join", "Connect", "j", "J"])
    async def join_command(self, ctx: commands.Context, channel: typing.Optional[discord.VoiceChannel]):
        if (ctx.author.id == 00000000000000):
            if ctx.author.voice is None:
                return await ctx.reply(embed=discord.Embed(title="You need to be in a voice channel to use this command", color=discord.Color.from_rgb(255, 255, 255)))
            
            if channel is None:
                channel = ctx.author.voice.channel
            
            node = wavelink.NodePool.get_node()
            player = node.get_player(ctx.guild.id)
            self.playingTextChannel = ctx.channel.id

            if player is not None:
                if player.is_connected():
                    return await ctx.reply(embed=discord.Embed(title="I'm already connected to a voice channel", color=discord.Color.from_rgb(255, 255, 255)))
            
            await channel.connect(cls=wavelink.Player)
            mbed=discord.Embed(title=f"Connected to {channel.name}", color=discord.Color.from_rgb(255, 255, 255))
            await ctx.send(embed=mbed)

    @commands.command(name="leave", aliases=["disconnect", "d", "Leave", "D", "Disconnect"])
    async def leave_command(self, ctx: commands.Context):
        if (ctx.author.id == 330308326758023169):
            node = wavelink.NodePool.get_node()
            player = node.get_player(ctx.guild.id)

            if player is None:
                return await ctx.reply(embed=discord.Embed(title="I'm not connected to any voice channel", color=discord.Color.from_rgb(255, 255, 255)))
            
            await player.disconnect()
            self.playingTextChannel = -1
            mbed = discord.Embed(title="Disconnected", color=discord.Color.from_rgb(255, 255, 255))
            await ctx.send(embed=mbed)

    @commands.command(name="ff", aliases=["FF", "FastForward", "fastForward", "Fastforward", "fastforward", "fF", "Ff"])
    async def fast_forward(self, ctx: commands.Context, seconds):
        if (ctx.channel.id == 0000000000000) or (ctx.channel.id == 0000000000000) or (ctx.channel.id == 0000000000000):
            if (ctx.author.voice == None):
                return await ctx.reply(embed=discord.Embed(title="You need to be in a voice channel to use this command", color=discord.Color.from_rgb(255, 255, 255)))
            elif ctx.voice_client==None:
                return await ctx.reply(embed=discord.Embed(title="Nothing is being played right now", color=discord.Color.from_rgb(255, 255, 255)))
            elif ctx.author.voice.channel != ctx.voice_client.channel:
                return await ctx.reply(embed=discord.Embed(title="You need to be in the same voice channel as me to use this command", color=discord.Color.from_rgb(255, 255, 255)))
            
            node = wavelink.NodePool.get_node()
            player = node.get_player(ctx.guild.id)
            
            try:
                seconds = int(seconds)
            except:
                return await ctx.reply(embed=discord.Embed(title="Sorry, but please give me a number without decimals", color=discord.Color.from_rgb(255, 255, 255)))
            
            new_position = (player.position//1000) + seconds
            await player.seek(new_position * 1000)
            return await ctx.reply(embed=discord.Embed(title="Song fast forwarded {} seconds".format(seconds), color=discord.Color.from_rgb(255, 255, 255)))
        else:
            return await ctx.reply(embed=discord.Embed(title="", description="Whoops, looks like you can't use this here. Try using it in <#879178001873502262>", color=discord.Color.from_rgb(255, 255, 255)))

    @commands.command(name="gb", aliases=["GB", "gB", "Gb", "GoBack", "goBack", "Goback", "goback"])
    async def go_back(self, ctx: commands.Context, seconds):
        if (ctx.channel.id == 0000000000000) or (ctx.channel.id == 0000000000000) or (ctx.channel.id == 0000000000000):
            if (ctx.author.voice == None):
                return await ctx.reply(embed=discord.Embed(title="You need to be in a voice channel to use this command", color=discord.Color.from_rgb(255, 255, 255)))
            elif ctx.voice_client==None:
                return await ctx.reply(embed=discord.Embed(title="Nothing is being played right now", color=discord.Color.from_rgb(255, 255, 255)))
            elif ctx.author.voice.channel != ctx.voice_client.channel:
                return await ctx.reply(embed=discord.Embed(title="You need to be in the same voice channel as me to use this command", color=discord.Color.from_rgb(255, 255, 255)))
            
            node = wavelink.NodePool.get_node()
            player = node.get_player(ctx.guild.id)
            
            try:
                seconds = int(seconds)
            except:
                return await ctx.reply(embed=discord.Embed(title="Sorry, but please give me a number without decimals", color=discord.Color.from_rgb(255, 255, 255)))
            
            new_position = (player.position//1000) - seconds
            await player.seek(new_position * 1000)
            return await ctx.reply(embed=discord.Embed(title="Song rewinded {} seconds".format(seconds), color=discord.Color.from_rgb(255, 255, 255)))
        else:
            return await ctx.reply(embed=discord.Embed(title="", description="Whoops, looks like you can't use this here. Try using it in <#879178001873502262>", color=discord.Color.from_rgb(255, 255, 255)))

    @commands.command(name="seek", aliases=["Seek", "tp", "Tp", "tP", "TP", "goto", "Goto", "GoTo", "goTo"])
    async def seek_command(self, ctx: commands.Context, minute: str=""):
        if (ctx.channel.id == 0000000000000) or (ctx.channel.id == 0000000000000) or (ctx.channel.id == 0000000000000):
            node = wavelink.NodePool.get_node()
            player = node.get_player(ctx.guild.id)
            
            if (ctx.author.voice == None):
                return await ctx.reply(embed=discord.Embed(title="You need to be in a voice channel to use this command", color=discord.Color.from_rgb(255, 255, 255)))
            elif ctx.voice_client==None:
                return await ctx.reply(embed=discord.Embed(title="Nothing is being played right now", color=discord.Color.from_rgb(255, 255, 255)))
            elif ctx.author.voice.channel != ctx.voice_client.channel:
                return await ctx.reply(embed=discord.Embed(title="You need to be in the same voice channel as me to use this command", color=discord.Color.from_rgb(255, 255, 255)))
            elif (player.is_paused()==False) and (player.is_playing()==False):
                return await ctx.reply(embed=discord.Embed(title="Nothing is being played right now", color=discord.Color.from_rgb(255, 255, 255)))
            
            if minute == "":
                return await ctx.reply(embed=discord.Embed(title="Sorry, but please give me the minute of the video", color=discord.Color.from_rgb(255, 255, 255)))
            try:
                if ((len(minute)==5) and (minute[2]==":")):
                    seconds = ((int(minute[0:2]))*60) + (int(minute[3:5]))
                    new_position = seconds
                    await player.seek(new_position * 1000)
                    return await ctx.reply(embed=discord.Embed(title="Song is at {}:{}".format(minute[0:2], minute[3:5]), color=discord.Color.from_rgb(255, 255, 255)))
                elif ((len(minute)==4) and (minute[1]==":")):
                    seconds = ((int(minute[0:1]))*60) + (int(minute[2:4]))
                    new_position = seconds
                    await player.seek(new_position * 1000)
                    return await ctx.reply(embed=discord.Embed(title="Song is at 0{}:{}".format(minute[0:1], minute[2:4]), color=discord.Color.from_rgb(255, 255, 255)))
                elif ((len(minute)==3) and (minute[1]==":")):
                    seconds = ((int(minute[0:1]))*60) + (int(minute[2:3]))
                    new_position = seconds
                    await player.seek(new_position * 1000)
                    return await ctx.reply(embed=discord.Embed(title="Song is at 0{}:0{}".format(minute[0:1], minute[2:4]), color=discord.Color.from_rgb(255, 255, 255)))
                elif (len(minute)==7) and (minute[1]==":") and (minute[4]==":"):
                    seconds = ((int(minute[0:1]))*3600) + ((int(minute[2:4]))*60) + (int(minute[5:7]))
                    new_position = seconds
                    await player.seek(new_position * 1000)
                    return await ctx.reply(embed=discord.Embed(title="Song is at {}:{}:{}".format(minute[0:1], minute[2:4], minute[5:7]), color=discord.Color.from_rgb(255, 255, 255)))
                elif (len(minute)==8) and (minute[2]==":") and (minute[5]==":"):
                    seconds = ((int(minute[0:2]))*3600) + ((int(minute[3:5]))*60) + (int(minute[6:8]))
                    new_position = seconds
                    await player.seek(new_position * 1000)
                    return await ctx.reply(embed=discord.Embed(title="Song is at {}:{}:{}".format(minute[0:2], minute[3:5], minute[6:8]), color=discord.Color.from_rgb(255, 255, 255)))
                
                else:
                    return await ctx.reply(embed=discord.Embed(title="Incorrect format, please try again with a mm:ss format or a hh:mm:ss format", color=discord.Color.from_rgb(255, 255, 255)))

            except:
                return await ctx.reply(embed=discord.Embed(title="Sorry, but please give me the minute of the video in a 'mm:ss' or a 'hh:mm:ss' format", color=discord.Color.from_rgb(255, 255, 255)))
        else:
            return await ctx.reply(embed=discord.Embed(title="", description="Whoops, looks like you can't use this here. Try using it in <#879178001873502262>", color=discord.Color.from_rgb(255, 255, 255)))

    @commands.command(name="clear", aliases=["Clear", "cl", "Cl", "CL", "cL", "CLS", "Cls", "cls"])
    async def clear_command(self, ctx: commands.Context):
        if (ctx.channel.id == 0000000000) or (ctx.channel.id == 00000000000000) or (ctx.channel.id == 879178001500221449):
            if (ctx.author.voice == None):
                return await ctx.reply(embed=discord.Embed(title="You need to be in a voice channel to use this command", color=discord.Color.from_rgb(255, 255, 255)))
            elif ctx.voice_client==None:
                return await ctx.reply(embed=discord.Embed(title="Nothing is being played right now", color=discord.Color.from_rgb(255, 255, 255)))
            elif ctx.author.voice.channel != ctx.voice_client.channel:
                return await ctx.reply(embed=discord.Embed(title="You need to be in the same voice channel as me to use this command", color=discord.Color.from_rgb(255, 255, 255)))

            if len(self.queue) <= 0:
                return await ctx.reply(embed=discord.Embed(title="The queue is empty", color=discord.Color.from_rgb(255, 255, 255)))

            self.queue.clear()
            return await ctx.reply(embed=discord.Embed(title="Queue Cleared", color=discord.Color.from_rgb(255, 255, 255)))
        else:
            return await ctx.reply(embed=discord.Embed(title="", description="Whoops, looks like you can't use this here. Try using it in <#879178001873502262>", color=discord.Color.from_rgb(255, 255, 255)))

    @commands.command(name="remove", aliases=["Remove", "rm", "RM", "Rm", "rM"])
    async def remove_command(self, ctx: commands.Context, index: str="-1"):
        if (ctx.channel.id == 0000000000000) or (ctx.channel.id == 0000000000000) or (ctx.channel.id == 0000000000000):
            if (ctx.author.voice == None):
                return await ctx.reply(embed=discord.Embed(title="You need to be in a voice channel to use this command", color=discord.Color.from_rgb(255, 255, 255)))
            elif ctx.voice_client==None:
                return await ctx.reply(embed=discord.Embed(title="Nothing is being played right now", color=discord.Color.from_rgb(255, 255, 255)))
            elif ctx.author.voice.channel != ctx.voice_client.channel:
                return await ctx.reply(embed=discord.Embed(title="You need to be in the same voice channel as me to use this command", color=discord.Color.from_rgb(255, 255, 255)))
            
            if len(self.queue) <= 0:
                return await ctx.reply(embed=discord.Embed(title="Sorry, but the queue is empty", color=discord.Color.from_rgb(255, 255, 255)))

            
            try:
                index = int(index)
                if index == 0:
                    return await ctx.reply(embed=discord.Embed(title="Sorry, but 0 is not a valid position", color=discord.Color.from_rgb(255, 255, 255)))
                elif index > 0:
                    if index > len(self.queue):
                        return await ctx.reply(embed=discord.Embed(title="Sorry, but the queue is not that long!", color=discord.Color.from_rgb(255, 255, 255)))
                elif index < 0:
                    if index + len(self.queue) < 0:
                        return await ctx.reply(embed=discord.Embed(title="Sorry, but the queue is not that long!", color=discord.Color.from_rgb(255, 255, 255)))       
            except:
                return await ctx.reply(embed=discord.Embed(title="Please enter a valid number of the position of the song you want to remove in the queue", color=discord.Color.from_rgb(255, 255, 255)))

            if index < 0:
                await ctx.reply(embed=discord.Embed(title="Removed from the queue:\n{}".format(self.queue[index]), color=discord.Color.from_rgb(255, 255, 255)))
                return self.queue.pop(index)
            elif index > 0:
                await ctx.reply(embed=discord.Embed(title="Removed from the queue:\n{}".format(self.queue[index-1]), color=discord.Color.from_rgb(255, 255, 255)))
                return self.queue.pop(index-1)
            else:
                return await ctx.reply(embed=discord.Embed(title="Whoops, looks like something went wrong!! Try again please".format(self.queue[index]), color=discord.Color.from_rgb(255, 255, 255)))
        else:
            return await ctx.reply(embed=discord.Embed(title="", description="Whoops, looks like you can't use this here. Try using it in <#879178001873502262>", color=discord.Color.from_rgb(255, 255, 255)))
        
    @commands.command(name="play", aliases=["p", "Play", "P"])
    async def play_command(self, ctx: commands.Context, *, search: str=""):
        if (ctx.channel.id == 0000000000000) or (ctx.channel.id == 0000000000000) or (ctx.channel.id == 0000000000000):
            if ctx.author.voice is None:
                return await ctx.reply(embed=discord.Embed(title="You need to be in a voice channel to use this command", color=discord.Color.from_rgb(255, 255, 255)))
            
            self.playingTextChannel = ctx.channel.id
            
            node = wavelink.NodePool.get_node()
            player = node.get_player(ctx.guild.id)
            
            if search == "":
                if ctx.voice_client==None:
                    return await ctx.reply(embed=discord.Embed(title="Nothing is being played right now", color=discord.Color.from_rgb(255, 255, 255)))
                elif ctx.author.voice.channel != ctx.voice_client.channel:
                    return await ctx.reply(embed=discord.Embed(title="You need to be in the same voice channel as me to use this command", color=discord.Color.from_rgb(255, 255, 255)))
                
                if not player.is_paused():
                    if player.is_playing():
                        await player.pause()
                        mbed = discord.Embed(title="Playback Paused", color=discord.Color.from_rgb(255, 255, 255))
                        return await ctx.send(embed=mbed)
                elif player.is_paused():
                    await player.resume()
                    mbed = discord.Embed(title="Playback Resumed", color=discord.Color.from_rgb(255, 255, 255))
                    return await ctx.send(embed=mbed)

            purpose = ""

            try:
                if ("www.youtube.com/playlist" in search) or ("music.youtube.com/playlist" in search):
                    try:
                        search = await wavelink.YouTubePlaylist.search(search)
                        search = search.tracks
                        comprobar = False
                        if len(self.queue) > 0:
                            comprobar = True
                        for i in search:
                            self.queue.append(i)
                        if not comprobar:
                            search = [self.queue[0]]
                        purpose = "playlist"
                    except:
                        return await ctx.reply(embed=discord.Embed(title="Whoops, something went wrong. If the playlist contains YouTubeMusic music-video links, I won't be able to accept it yet (working on a solution). If that's not the case please contact Coder#0001 to try to solve it", color=discord.Color.from_rgb(255, 255, 255)))
                            
                elif ("www.youtube.com/watch" in search):
                    if ("&list=" in search):
                        search = search.split("&list=")
                        search = search[0]
                        
                    try:
                        search = await wavelink.YouTubeTrack.search(search)
                        purpose = "track"
                    except:
                        return await ctx.reply(embed=discord.Embed(title="I'm sorry, but it looks like I couldn't search for the song...", color=discord.Color.from_rgb(255, 255, 255)))
                
                elif ("music.youtube.com/watch" in search):
                    try:
                        search = await wavelink.YouTubeMusicTrack.search(search)
                        purpose="track"
                    except:
                        return await ctx.reply(embed=discord.Embed(title="Whoops, something went wrong. I currently accept YouTubeMusic tracks, albums and playlists, but not music-video links (working on a solution). I'm sorry :(", color=discord.Color.from_rgb(255, 255, 255)))

                elif ("soundcloud.com" in search):
                    return await ctx.reply(embed=discord.Embed(title="I'm sorry, but SoundCloud is not compatible for now :(", color=discord.Color.from_rgb(255, 255, 255)))
                
                elif ("open.spotify.com/track" in search):
                    try:
                        track_name = self.get_the_track(the_track_id=search)
                        search = await wavelink.YouTubeTrack.search(track_name)
                        purpose = "track"
                    except:
                        return await ctx.reply(embed=discord.Embed(title="Whoops, looks like something went wrong while searching for this track...", color=discord.Color.from_rgb(255, 255, 255)))

                elif ("open.spotify.com/playlist" in search):
                    try:
                        track_playlist = self.get_playlist_tracks(the_playlist_id=search)
                        search = await wavelink.YouTubeTrack.search(track_playlist[0])
                        comprobar = False
                        if len(self.queue) > 0:
                            comprobar = True
                        for i in track_playlist:
                            self.queue.append(i)
                        if not comprobar:
                            search = await wavelink.YouTubeTrack.search(self.queue[0])
                        purpose = "playlist"
                    except:
                        return await ctx.reply(embed=discord.Embed(title="Whoops, looks like something went wrong while searching for this track...", color=discord.Color.from_rgb(255, 255, 255)))
                
                elif ("open.spotify.com/album" in search):
                    try:
                        track_album = self.get_album_tracks(the_album_id=search)
                        search = await wavelink.YouTubeTrack.search(track_album[0])
                        comprobar = False
                        if len(self.queue) > 0:
                            comprobar = True
                        for i in track_album:
                            self.queue.append(i)
                        if not comprobar:
                            search = await wavelink.YouTubeTrack.search(self.queue[0])
                        purpose = "album"
                    except:
                        return await ctx.reply(embed=discord.Embed(title="Whoops, looks like something went wrong while searching for this track...", color=discord.Color.from_rgb(255, 255, 255)))
                
                elif ("deezer.page.link/" in search) or ("www.deezer.com/" in search):
                    temporal = requests.request(method="GET", url="https://api.deezer.com/oembed?url={}".format(search))
                    temporal = temporal.json()
                    type = temporal["entity"]

                    if type == "track":
                        final_track = "{} - {}".format(temporal["author_name"], temporal["title"])
                        try:
                            search = await wavelink.YouTubeTrack.search(final_track)
                            purpose = "track"
                        except:
                            return await ctx.reply(embed=discord.Embed(title="Whoops, looks like something went wrong while searching for this track...", color=discord.Color.from_rgb(255, 255, 255)))

                    elif type == "playlist":
                        temporal_list = []
                        id = temporal["id"]
                        playlist = requests.request(method="GET", url="https://api.deezer.com/playlist/{}".format(id))
                        playlist = playlist.json()
                        playlist = playlist["tracks"]["data"]
                        for i in playlist:
                            temporal_list.append("{} - {}".format(i["title"], i["artist"]["name"]))

                        comprobar = False
                        if len(self.queue) > 0:
                            comprobar = True
                        for i in temporal_list:
                            self.queue.append(i)
                        if not comprobar:
                            search = await wavelink.YouTubeTrack.search(self.queue[0])
                        purpose = "playlist"
                        
                    elif type == "album":
                        temporal_list = []
                        id = temporal["id"]
                        album = requests.request(method="GET", url="https://api.deezer.com/album/{}".format(id))
                        album = album.json()
                        album = album["tracks"]["data"]
                        for i in album:
                            temporal_list.append("{} - {}".format(i["title"], i["artist"]["name"]))

                        comprobar = False
                        if len(self.queue) > 0:
                            comprobar = True
                        for i in temporal_list:
                            self.queue.append(i)
                        if not comprobar:
                            search = await wavelink.YouTubeTrack.search(self.queue[0])
                        purpose = "album"

                else:
                    search = await wavelink.YouTubeTrack.search(search)
                    purpose = "track"
            except:
                return await ctx.reply(embed=discord.Embed(title="Something went wrong while searching for this track", color=discord.Color.from_rgb(255, 255, 255)))

            if not ctx.voice_client:
                vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        
            else:
                vc: wavelink.Player = ctx.voice_client
            

            if not vc.is_playing():
                try:
                    await vc.play(search[0])
                except:
                    return await ctx.reply(embed=discord.Embed(title="Something went wrong while playing this track", color=discord.Color.from_rgb(255, 255, 255)))
            else:
                self.queue.append(search[0])

            if (purpose == "track"):
                mbed = discord.Embed(title=f"Added {search[0]} To the queue", color=discord.Color.from_rgb(255, 255, 255))
                await ctx.send(embed=mbed)
            elif (purpose == "playlist"):
                mbed = discord.Embed(title="Playlist Added To The Queue", color=discord.Color.from_rgb(255, 255, 255))
                await ctx.send(embed=mbed)
            elif (purpose == "album"):
                mbed = discord.Embed(title="Album Added To The Queue", color=discord.Color.from_rgb(255, 255, 255))
                await ctx.send(embed=mbed)
        else:
            return await ctx.reply(embed=discord.Embed(title="", description="Whoops, looks like you can't use this here. Try using it in <#879178001873502262>", color=discord.Color.from_rgb(255, 255, 255)))

    @commands.command(name="loop", aliases=["Loop"])
    async def loop_command(self, ctx: commands.Command, mode: str=""):
        if (ctx.channel.id == 0000000000000) or (ctx.channel.id == 0000000000000) or (ctx.channel.id == 0000000000000):
            if (ctx.author.voice == None):
                return await ctx.reply(embed=discord.Embed(title="You need to be in a voice channel to use this command", color=discord.Color.from_rgb(255, 255, 255)))
            elif ctx.voice_client==None:
                return await ctx.reply(embed=discord.Embed(title="Nothing is being played right now", color=discord.Color.from_rgb(255, 255, 255)))
            elif ctx.author.voice.channel != ctx.voice_client.channel:
                return await ctx.reply(embed=discord.Embed(title="You need to be in the same voice channel as me to use this command", color=discord.Color.from_rgb(255, 255, 255)))
            
            node = wavelink.NodePool.get_node()
            player = node.get_player(ctx.guild.id)

            if player is None:
                return await ctx.reply(embed=discord.Embed(title="Sorry, but I'm not connected to any voice channel :(", color=discord.Color.from_rgb(255, 255, 255)))

            if mode=="" or mode.lower()=="track":
                if self.looping_track == True:
                    return await ctx.reply(embed=discord.Embed(title="Track is already in a Loop", color=discord.Color.from_rgb(255, 255, 255)))
                self.looping_track = True
                self.looping_queue = False
                self.looped_track = player.current
                self.queue_index_in_loop = 0
                return await ctx.reply(embed=discord.Embed(title="Current Track Looped", color=discord.Color.from_rgb(255, 255, 255)))
            elif mode.lower()=="queue" or mode.lower()=="all" or mode.lower()=="q":
                if self.looping_queue == True:
                    return await ctx.reply(embed=discord.Embed(title="The Queue is already in a Loop", color=discord.Color.from_rgb(255, 255, 255)))
                self.looping_track = False
                self.looping_queue = True
                self.queue_index_in_loop = 0
                self.queue.append(player.current)
                self.looped_track = ""
                return await ctx.reply(embed=discord.Embed(title="Current Track and Queue Looped", color=discord.Color.from_rgb(255, 255, 255)))
            elif mode.lower()=="off" or mode.lower()=="disable":
                if self.looping_track == False and self.looping_queue == False:
                    return await ctx.reply(embed=discord.Embed(title="There is Nothing being Looped", color=discord.Color.from_rgb(255, 255, 255)))

                self.looping_track = False
                self.looping_queue = False
                self.looped_track = ""
                self.queue_index_in_loop = 0
                return await ctx.reply(embed=discord.Embed(title="Getting out of the loop", color=discord.Color.from_rgb(255, 255, 255)))
        
        else:
            return await ctx.reply(embed=discord.Embed(title="", description="Whoops, looks like you can't use this here. Try using it in <#879178001873502262>", color=discord.Color.from_rgb(255, 255, 255)))


    @commands.command(name="stop", aliases=["Stop"])
    async def stop_command(self, ctx: commands.Context):
        if (ctx.channel.id == 0000000000000) or (ctx.channel.id == 0000000000000) or (ctx.channel.id == 0000000000000):
            node = wavelink.NodePool.get_node()
            player = node.get_player(ctx.guild.id)

            if player is None:
                return await ctx.reply(embed=discord.Embed(title="Sorry, but I'm not connected to any voice channel :(", color=discord.Color.from_rgb(255, 255, 255)))

            self.queue.clear()
            self.looping_track = False
            self.looping_queue = False
            self.looped_track = ""
            self.queue_index_in_loop = 0
            
            if player.is_playing():
                await player.stop()
                await player.disconnect()
                return await ctx.reply(embed=discord.Embed(title="Playback Stopped\nDisconnected", color=discord.Color.from_rgb(255, 255, 255))) 
            else:
                return await ctx.reply(embed=discord.Embed(title="Nothing is being played right now", color=discord.Color.from_rgb(255, 255, 255)))
        else:
            return await ctx.reply(embed=discord.Embed(title="", description="Whoops, looks like you can't use this here. Try using it in <#879178001873502262>", color=discord.Color.from_rgb(255, 255, 255)))

    @commands.command(name="pause", aliases=["Pause"])
    async def pause_command(self, ctx: commands.Context):
        if (ctx.channel.id == 0000000000000) or (ctx.channel.id == 0000000000000) or (ctx.channel.id == 0000000000000):
            if (ctx.author.voice == None):
                return await ctx.reply(embed=discord.Embed(title="You need to be in a voice channel to use this command", color=discord.Color.from_rgb(255, 255, 255)))
            elif ctx.voice_client==None:
                return await ctx.reply(embed=discord.Embed(title="Nothing is being played right now", color=discord.Color.from_rgb(255, 255, 255)))
            elif ctx.author.voice.channel != ctx.voice_client.channel:
                return await ctx.reply(embed=discord.Embed(title="You need to be in the same voice channel as me to use this command", color=discord.Color.from_rgb(255, 255, 255)))
            
            node = wavelink.NodePool.get_node()
            player = node.get_player(ctx.guild.id)

            if player is None:
                return await ctx.reply(embed=discord.Embed(title="Sorry, but I'm not connected to any voice channel :(", color=discord.Color.from_rgb(255, 255, 255)))
            
            if not player.is_paused():
                if player.is_playing():
                    await player.pause()
                    mbed = discord.Embed(title="Playback Paused", color=discord.Color.from_rgb(255, 255, 255))
                    return await ctx.send(embed=mbed)
                else:
                    return await ctx.reply(embed=discord.Embed(title="Nothing is being played right now", color=discord.Color.from_rgb(255, 255, 255)))
            else:
                return await ctx.reply(embed=discord.Embed(title="Playback is Already paused", color=discord.Color.from_rgb(255, 255, 255)))
        else:
            return await ctx.reply(embed=discord.Embed(title="", description="Whoops, looks like you can't use this here. Try using it in <#879178001873502262>", color=discord.Color.from_rgb(255, 255, 255)))

    @commands.command(name="resume", aliases=["Resume"])
    async def resume_command(self, ctx: commands.Context):
        if (ctx.channel.id == 0000000000000) or (ctx.channel.id == 0000000000000) or (ctx.channel.id == 0000000000000):
            if (ctx.author.voice == None):
                return await ctx.reply(embed=discord.Embed(title="You need to be in a voice channel to use this command", color=discord.Color.from_rgb(255, 255, 255)))
            elif ctx.voice_client==None:
                return await ctx.reply(embed=discord.Embed(title="Nothing is being played right now", color=discord.Color.from_rgb(255, 255, 255)))
            elif ctx.author.voice.channel != ctx.voice_client.channel:
                return await ctx.reply(embed=discord.Embed(title="You need to be in the same voice channel as me to use this command", color=discord.Color.from_rgb(255, 255, 255)))
            
            node = wavelink.NodePool.get_node()
            player = node.get_player(ctx.guild.id)

            if player is None:
                return await ctx.reply(embed=discord.Embed(title="Sorry, but I'm not connected to any voice channel :(", color=discord.Color.from_rgb(255, 255, 255)))
            
            if (player.is_paused()==False) and (player.is_playing()==False) and (self.playingTextChannel != -1):
                if not len(self.queue) == 0:
                    if isinstance(self.queue[0], str):
                        next_track = await wavelink.YouTubeTrack.search(self.queue[0])
                        next_track = next_track[0]
                    else:
                        next_track: wavelink.YouTubeTrack = self.queue[0]

                    try:
                        await player.play(next_track)
                    except:
                        return await ctx.reply(embed=discord.Embed(title="Something went wrong while playing this track", color=discord.Color.from_rgb(255, 255, 255)))

                    await ctx.reply(embed=discord.Embed(title=f"Now playing {next_track[0].title}", color=discord.Color.from_rgb(255, 255, 255)))
                else:
                    await ctx.reply(embed=discord.Embed(title="The queue is empty", color=discord.Color.from_rgb(255, 255, 255)))
            elif player.is_paused():
                await player.resume()
                mbed = discord.Embed(title="Playback resumed", color=discord.Color.from_rgb(255, 255, 255))
                return await ctx.send(embed=mbed)
            else:
                return await ctx.reply(embed=discord.Embed(title="Playback is not paused", color=discord.Color.from_rgb(255, 255, 255)))
        else:
            return await ctx.reply(embed=discord.Embed(title="", description="Whoops, looks like you can't use this here. Try using it in <#879178001873502262>", color=discord.Color.from_rgb(255, 255, 255)))

    @commands.command(name="shuffle", aliases=["Shuffle"])
    async def shuffle_playlist(self, ctx: commands.Context):
        if (ctx.channel.id == 0000000000000) or (ctx.channel.id == 0000000000000) or (ctx.channel.id == 0000000000000):
            if (ctx.author.voice == None):
                return await ctx.reply(embed=discord.Embed(title="You need to be in a voice channel to use this command", color=discord.Color.from_rgb(255, 255, 255)))
            elif ctx.voice_client==None:
                return await ctx.reply(embed=discord.Embed(title="Nothing is being played right now", color=discord.Color.from_rgb(255, 255, 255)))
            elif ctx.author.voice.channel != ctx.voice_client.channel:
                return await ctx.reply(embed=discord.Embed(title="You need to be in the same voice channel as me to use this command", color=discord.Color.from_rgb(255, 255, 255)))
            
            if len(self.queue)==0:
                return await ctx.reply(embed=discord.Embed(title="Whoops, looks like the playlist is empty... Try adding some songs to it!!", color=discord.Color.from_rgb(255, 255, 255)))
            if len(self.queue)==1:
                return await ctx.reply(embed=discord.Embed(title="I guess I can shuffle a playlist with just one song, but it won't change the order too much...", color=discord.Color.from_rgb(255, 255, 255)))
            
            random.shuffle(self.queue)
            return await ctx.reply(embed=discord.Embed(title="Playlist Shuffled", color=discord.Color.from_rgb(255, 255, 255)))
        else:
            return await ctx.reply(embed=discord.Embed(title="", description="Whoops, looks like you can't use this here. Try using it in <#879178001873502262>", color=discord.Color.from_rgb(255, 255, 255)))

    @commands.command(name="nowplaying", aliases=["now_playing", "np", "NowPlaying", "Nowplaying", "nowPlaying", "NP"])
    async def now_playing_command(self, ctx: commands.Context):
        if (ctx.channel.id == 0000000000000) or (ctx.channel.id == 0000000000000) or (ctx.channel.id == 0000000000000) or (ctx.channel.id == 0000000000000):
            if (ctx.author.voice == None):
                return await ctx.reply(embed=discord.Embed(title="You need to be in a voice channel to use this command", color=discord.Color.from_rgb(255, 255, 255)))
            elif ctx.voice_client==None:
                return await ctx.reply(embed=discord.Embed(title="Nothing is being played right now", color=discord.Color.from_rgb(255, 255, 255)))
            elif ctx.author.voice.channel != ctx.voice_client.channel:
                return await ctx.reply(embed=discord.Embed(title="You need to be in the same voice channel as me to use this command", color=discord.Color.from_rgb(255, 255, 255)))
            
            node = wavelink.NodePool.get_node()
            player = node.get_player(ctx.guild.id)

            if (player.is_paused()==False) and (player.is_playing()==False):
                return await ctx.reply(embed=discord.Embed(title="Nothing is being played right now", color=discord.Color.from_rgb(255, 255, 255)))

            if player is None:
                return await ctx.reply(embed=discord.Embed(title="Sorry, but I'm not connected to any voice channel :(", color=discord.Color.from_rgb(255, 255, 255)))

            if player.is_playing():
                mbed = discord.Embed(
                    title=f"Now Playing: {player.current}",
                    #you can add url as one the arugument over here, if you want the user to be able to open the video in youtube
                    #url = f"{player.track.info['uri']}"
                    color=discord.Color.from_rgb(255, 255, 255)
                )

                t_sec = int(player.current.length)/1000
                hour = int(t_sec/3600)
                minute = int((t_sec%3600)/60)
                sec = int((t_sec%3600)%60)
                if sec < 10:
                    sec = "0{}".format(sec)
                if minute < 10:
                    minute = "0{}".format(minute)
                length = f"{hour}:{minute}:{sec}" if not hour == 0 else f"{minute}:{sec}"

                thumb = await player.current.fetch_thumbnail()
                mbed.set_thumbnail(url=thumb)
                mbed.add_field(name="", value="")
                mbed.add_field(name="Channel or Artist", value="{}".format(player.current.author), inline=False)
                mbed.add_field(name="", value="")
                mbed.add_field(name="Length", value=f"{length}", inline=False)

                return await ctx.reply(embed=mbed)
            else:
                return await ctx.reply(embed=discord.Embed(title="Nothing is playing right now", color=discord.Color.from_rgb(255, 255, 255)))
        else:
            return await ctx.reply(embed=discord.Embed(title="", description="Whoops, looks like you can't use this here. Try using it in <#879178001873502262>", color=discord.Color.from_rgb(255, 255, 255)))

    @commands.command(name="search", aliases=["Search"])
    async def search_command(self, ctx: commands.Context, *, search: str):
        if (ctx.channel.id == 0000000000000) or (ctx.channel.id == 0000000000000) or (ctx.channel.id == 0000000000000):
            if (ctx.author.voice == None):
                return await ctx.reply(embed=discord.Embed(title="You need to be in a voice channel to use this command", color=discord.Color.from_rgb(255, 255, 255)))
            
            try:
                tracks = await wavelink.YouTubeTrack.search(search)
            except:
                return await ctx.reply(embed=discord.Embed(title="Something went wrong while searching for this track", color=discord.Color.from_rgb(255, 255, 255)))

            if tracks is None:
                return await ctx.reply(embed=discord.Embed(title="Please write a title of a song or a video", color=discord.Color.from_rgb(255, 255, 255)))

            node = wavelink.NodePool.get_node()
            player = node.get_player(ctx.guild.id)

            mbed = discord.Embed(
                title="Select the track: ",
                description=("\n".join(f"**{i+1}. {t.title}**" for i, t in enumerate(tracks[:5]))),
                color = discord.Color.from_rgb(255, 255, 255)
            )
            msg = await ctx.reply(embed=mbed)

            emojis_list = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '❌']
            emojis_dict = {
                '1️⃣': 0,
                "2️⃣": 1,
                "3️⃣": 2,
                "4️⃣": 3,
                "5️⃣": 4,
                "❌": -1
            }

            for emoji in list(emojis_list[:min(len(tracks), len(emojis_list))]):
                await msg.add_reaction(emoji)

            def check(res, user):
                return(res.emoji in emojis_list and user == ctx.author and res.message.id == msg.id)

            try:
                reaction, _ = await self.bot.wait_for("reaction_add", timeout=60.0, check=check)
            except asyncio.TimeoutError:
                await msg.delete()
                return
            else:
                await msg.delete()

            try:
                if emojis_dict[reaction.emoji] == -1: return
                chosen_track = tracks[emojis_dict[reaction.emoji]]
            except:
                return

            vc: wavelink.Player = ctx.voice_client or await ctx.author.voice.channel.connect(cls=wavelink.Player)

            if player is None:
                try:
                    await vc.play(chosen_track)
                except:
                    return await ctx.reply(embed=discord.Embed(title="Something went wrong while playing this track", color=discord.Color.from_rgb(255, 255, 255)))
            else:
                self.queue.append(chosen_track)
            
            await ctx.reply(embed=discord.Embed(title=f"Added {chosen_track[0].title} to the queue", color=discord.Color.from_rgb(255, 255, 255)))
        else:
            return await ctx.reply(embed=discord.Embed(title="", description="Whoops, looks like you can't use this here. Try using it in <#879178001873502262>", color=discord.Color.from_rgb(255, 255, 255)))

    @commands.command(name="skip", aliases=["Skip", "sk", "Sk", "SK", "sK"])
    async def skip_command(self, ctx: commands.Context):
        if (ctx.channel.id == 0000000000000) or (ctx.channel.id == 0000000000000) or (ctx.channel.id == 0000000000000):
            if (ctx.author.voice == None):
                return await ctx.reply(embed=discord.Embed(title="You need to be in a voice channel to use this command", color=discord.Color.from_rgb(255, 255, 255)))
            elif ctx.voice_client==None:
                return await ctx.reply(embed=discord.Embed(title="Nothing is being played right now", color=discord.Color.from_rgb(255, 255, 255)))
            elif ctx.author.voice.channel != ctx.voice_client.channel:
                return await ctx.reply(embed=discord.Embed(title="You need to be in the same voice channel as me to use this command", color=discord.Color.from_rgb(255, 255, 255)))
            
            node = wavelink.NodePool.get_node()
            player = node.get_player(ctx.guild.id)

            if self.looping_track==True or self.looping_queue==True:
                self.looping_track = False
                self.looping_queue = False
                self.looped_track = ""
                self.queue_index_in_loop = 0
                loop_state = "Getting out of the loop\n"
            else:
                loop_state = ""

            if not len(self.queue) == 0:
                if isinstance(self.queue[0], str):
                    next_track = await wavelink.YouTubeTrack.search(self.queue[0])
                    next_track = next_track[0]
                else:
                    next_track: wavelink.YouTubeTrack = self.queue[0]
                    
                try:
                    await player.play(next_track)
                except:
                    return await ctx.reply(embed=discord.Embed(title="Something went wrong while playing this track", color=discord.Color.from_rgb(255, 255, 255)))

                return await ctx.reply(embed=discord.Embed(title=f"{loop_state}Now playing {next_track.title}", color=discord.Color.from_rgb(255, 255, 255)))
            else:
                await player.stop()
                await player.disconnect()
                self.playingTextChannel = -1
                return await ctx.send(embed=discord.Embed(title="Playlist's over\nDisconnected", color=discord.Color.from_rgb(255, 255, 255)))
        else:
            return await ctx.reply(embed=discord.Embed(title="", description="Whoops, looks like you can't use this here. Try using it in <#879178001873502262>", color=discord.Color.from_rgb(255, 255, 255)))

    @commands.command(name="queue", aliases=["q", "Queue", "Q"])
    async def queue_command(self, ctx: commands.Context):
        if (ctx.channel.id == 0000000000000) or (ctx.channel.id == 0000000000000) or (ctx.channel.id == 0000000000000):
            node = wavelink.NodePool.get_node()
            player = node.get_player(ctx.guild.id)

            if (ctx.author.voice == None):
                return await ctx.reply(embed=discord.Embed(title="You need to be in a voice channel to use this command", color=discord.Color.from_rgb(255, 255, 255)))
            elif ctx.voice_client==None:
                return await ctx.reply(embed=discord.Embed(title="Nothing is being played right now", color=discord.Color.from_rgb(255, 255, 255)))
            elif ctx.author.voice.channel != ctx.voice_client.channel:
                return await ctx.reply(embed=discord.Embed(title="You need to be in the same voice channel as me to use this command", color=discord.Color.from_rgb(255, 255, 255)))
                        
            if not len(self.queue) == 0:
                t_d = self.queue
                t_t = "{}".format(player.current)
                t_thumb = await player.current.fetch_thumbnail()
                pagination_view = PaginationView()
                await pagination_view.get_data(t_thumb, t_d, t_t, ctx)
            else:
                return await ctx.reply(embed=discord.Embed(title="The queue is empty", color=discord.Color.from_rgb(255, 255, 255)))
        else:
            return await ctx.reply(embed=discord.Embed(title="", description="Whoops, looks like you can't use this here. Try using it in <#879178001873502262>", color=discord.Color.from_rgb(255, 255, 255)))
    
    @commands.command(name="restart", aliases=["Restart", "reset", "Reset", "replay", "Replay"])
    async def restart_command(self, ctx: commands.Context):
        if (ctx.channel.id == 0000000000000) or (ctx.channel.id == 0000000000000) or (ctx.channel.id == 0000000000000):
            if (ctx.author.voice == None):
                return await ctx.reply(embed=discord.Embed(title="You need to be in a voice channel to use this command", color=discord.Color.from_rgb(255, 255, 255)))
            elif ctx.voice_client==None:
                return await ctx.reply(embed=discord.Embed(title="Nothing is being played right now", color=discord.Color.from_rgb(255, 255, 255)))
            elif ctx.author.voice.channel != ctx.voice_client.channel:
                return await ctx.reply(embed=discord.Embed(title="You need to be in the same voice channel as me to use this command", color=discord.Color.from_rgb(255, 255, 255)))
            
            node = wavelink.NodePool.get_node()
            player = node.get_player(ctx.guild.id)

            await player.seek(1)
            return await ctx.reply(embed=discord.Embed(title="{} restarted".format(player.current.title), color=discord.Color.from_rgb(255, 255, 255)))
        else:
            return await ctx.reply(embed=discord.Embed(title="", description="Whoops, looks like you can't use this here. Try using it in <#879178001873502262>", color=discord.Color.from_rgb(255, 255, 255)))

    @commands.command(name="move", aliases=["Move"])
    async def move_command(self, ctx: commands.Context, number1: str=None, number2: str=None):
        if (ctx.channel.id == 0000000000000) or (ctx.channel.id == 0000000000000) or (ctx.channel.id == 0000000000000):
            if (ctx.author.voice == None):
                return await ctx.reply(embed=discord.Embed(title="You need to be in a voice channel to use this command", color=discord.Color.from_rgb(255, 255, 255)))
            elif ctx.voice_client==None:
                return await ctx.reply(embed=discord.Embed(title="Nothing is being played right now", color=discord.Color.from_rgb(255, 255, 255)))
            elif ctx.author.voice.channel != ctx.voice_client.channel:
                return await ctx.reply(embed=discord.Embed(title="You need to be in the same voice channel as me to use this command", color=discord.Color.from_rgb(255, 255, 255)))
            
            if number1==None or number2==None:
                return await ctx.reply(embed=discord.Embed(title="Please enter two valid numbers next to the command", color=discord.Color.from_rgb(255, 255, 255)))

            if len(self.queue) <= 0:
                return await ctx.reply(embed=discord.Embed(title="Sorry, but the queue is empty", color=discord.Color.from_rgb(255, 255, 255)))

            try:
                source = int(number1)
                destination = int(number2)

                if source == 0 or destination == 0:
                    return await ctx.reply(embed=discord.Embed(title="Sorry, but 0 is not a valid position", color=discord.Color.from_rgb(255, 255, 255)))
                elif source > 0:
                    if source > len(self.queue):
                        return await ctx.reply(embed=discord.Embed(title="Sorry, but the queue is not that long!", color=discord.Color.from_rgb(255, 255, 255)))
                elif source < 0:
                    if source + len(self.queue) < 0:
                        return await ctx.reply(embed=discord.Embed(title="Sorry, but the queue is not that long!", color=discord.Color.from_rgb(255, 255, 255)))

                temporal_position = self.queue[source-1]
                self.queue.pop(source-1)

                self.queue.insert(destination-1, temporal_position)
                return await ctx.reply(embed=discord.Embed(title="Track Moved From Position {} To {}".format(source, destination), color=discord.Color.from_rgb(255, 255, 255)))
            except:
                return await ctx.reply(embed=discord.Embed(title="Whoops, looks like something went wrong.\nPlease write two numbers without decimals to move a track in the queue", color=discord.Color.from_rgb(255, 255, 255)))
        else:
            return await ctx.reply(embed=discord.Embed(title="", description="Whoops, looks like you can't use this here. Try using it in <#879178001873502262>", color=discord.Color.from_rgb(255, 255, 255)))

    @commands.command(name="length", aliases=["Length"])
    async def check_length(self, ctx: commands.Context):
        if (ctx.author.voice == None):
            return await ctx.reply(embed=discord.Embed(title="You need to be in a voice channel to use this command", color=discord.Color.from_rgb(255, 255, 255)))
        elif ctx.voice_client==None:
            return await ctx.reply(embed=discord.Embed(title="Nothing is being played right now", color=discord.Color.from_rgb(255, 255, 255)))
        elif ctx.author.voice.channel != ctx.voice_client.channel:
            return await ctx.reply(embed=discord.Embed(title="You need to be in the same voice channel as me to use this command", color=discord.Color.from_rgb(255, 255, 255)))
            
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild.id)

        if (player.is_paused()==False) and (player.is_playing()==False):
            return await ctx.reply(embed=discord.Embed(title="Nothing is being played right now", color=discord.Color.from_rgb(255, 255, 255)))

        if player is None:
            return await ctx.reply(embed=discord.Embed(title="Sorry, but I'm not connected to any voice channel :(", color=discord.Color.from_rgb(255, 255, 255)))

        if player.is_playing():
            t_sec = int(player.current.length)/1000
            hour = int(t_sec/3600)
            minute = int((t_sec%3600)/60)
            sec = int((t_sec%3600)%60)
            if sec < 10:
                sec = "0{}".format(sec)
            if minute < 10:
                minute = "0{}".format(minute)
            length = f"{hour}:{minute}:{sec}" if not hour == 0 else f"{minute}:{sec}"

            t_sec = int(player.position)/1000
            hour = int(t_sec/3600)
            minute = int((t_sec%3600)/60)
            sec = int((t_sec%3600)%60)
            if sec < 10:
                sec = "0{}".format(sec)
            if minute < 10:
                minute = "0{}".format(minute)
            current_position = f"{hour}:{minute}:{sec}" if not hour == 0 else f"{minute}:{sec}"

            mbed = discord.Embed(title="Now at {}\n\nLength: {}".format(current_position, length), color=discord.Color.from_rgb(255, 255, 255))

            return await ctx.reply(embed=mbed)
        else:
            return await ctx.reply(embed=discord.Embed(title="Nothing is playing right now", color=discord.Color.from_rgb(255, 255, 255)))

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class PaginationView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.my_list = []
        self.the_thumbnail = ""
        self.the_track = ""
        self.my_context: commands.Context
        self.message = ""
        self.current_page: int = 1

    async def get_data(self, temporal_thumbnail, temporal_list, temporal_track, temporal_context: commands.Context):
        self.the_thumbnail = temporal_thumbnail
        self.the_track = temporal_track
        self.my_context = temporal_context

        multiple = len(temporal_list)//10
        resto = len(temporal_list)%10

        length_to_split = []

        for i in range (0, multiple):
            length_to_split.append(10)
        if resto > 0:
            length_to_split.append(resto)

        input = iter(temporal_list)
        output = [list(islice(input, element)) for element in length_to_split]

        self.my_list = output

        await self.send_message()

    async def send_message(self):
        self.message = await self.my_context.send(view=self)
        await self.update_message(self.my_list[self.current_page-1])
    
    def create_embed(self, data):
        embed = discord.Embed(title="Now Playing: {}".format(self.the_track), color=discord.Color.from_rgb(255, 255, 255))
        embed.set_thumbnail(url=self.the_thumbnail)
        for i in range (0, len(data)):
            embed.add_field(name="{}. {}".format(((self.current_page-1)*10) + (i+1), data[i]), value="", inline=False)
        embed.add_field(name=chr(173) ,value="\nPage {}/{}".format(self.current_page, len(self.my_list)), inline= False)
        return embed
    
    async def update_message(self, data):
        self.update_buttons()
        await self.message.edit(embed=self.create_embed(data), view=self)
    
    def update_buttons(self):

        if len(self.my_list)==1:
            self.first_page.disabled = True
            self.previous_button.disabled = True
            self.next_button.disabled = True
            self.last_page.disabled = True
        elif self.current_page == 1:
            self.first_page.disabled = True
            self.previous_button.disabled = True
            self.next_button.disabled = False
            self.last_page.disabled = False
        elif self.current_page == (len(self.my_list)):
            self.first_page.disabled = False
            self.previous_button.disabled = False
            self.next_button.disabled = True
            self.last_page.disabled = True
        else:
            self.first_page.disabled = False
            self.previous_button.disabled = False
            self.next_button.disabled = False
            self.last_page.disabled = False

    @discord.ui.button(label="|❮", style=discord.ButtonStyle.primary)
    async def first_page(self, interaction: discord.Interaction, button = discord.Button):
        await interaction.response.defer()
        self.current_page = 1
        await self.update_message(self.my_list[self.current_page-1])
    
    @discord.ui.button(label="❮", style=discord.ButtonStyle.primary)
    async def previous_button(self, interaction: discord.Interaction, button = discord.Button):
        await interaction.response.defer()
        self.current_page -= 1
        await self.update_message(self.my_list[self.current_page-1])
    
    @discord.ui.button(label="✗", style=discord.ButtonStyle.red)
    async def delete(self, interaction: discord.Interaction, button = discord.Button):
        await interaction.response.defer()
        await self.message.delete()
    
    @discord.ui.button(label="❯", style=discord.ButtonStyle.primary)
    async def next_button(self, interaction: discord.Interaction, button = discord.Button):
        await interaction.response.defer()
        self.current_page += 1
        await self.update_message(self.my_list[self.current_page-1])
    
    @discord.ui.button(label="❯|", style=discord.ButtonStyle.primary)
    async def last_page(self, interaction: discord.Interaction, button = discord.Button):
        await interaction.response.defer()
        self.current_page = (len(self.my_list))
        await self.update_message(self.my_list[self.current_page-1])

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class TemporaryVoice(commands.Cog):

    temporary_channels = []
    temporary_categories = []

    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        possible_channel = "{}'s Area".format(member.name)
        if after.channel:    
            if after.channel.name == "Voice":
                temp_channel = await after.channel.clone(name = possible_channel)
                await member.move_to(temp_channel)
                self.temporary_channels.append(temp_channel.id)
            if after.channel.name == "Voice + Text":
                temp_category = await after.channel.guild.create_category(name = possible_channel)
                await temp_category.create_text_channel(name="text")
                temp_channel = await temp_category.create_voice_channel(name="voice")
                await member.move_to(temp_channel)
                self.temporary_categories.append(temp_channel.id)

        if before.channel:    
            if before.channel.id in self.temporary_channels:
                if len(before.channel.members) == 0:
                    await before.channel.delete()
            if before.channel.id in self.temporary_categories:
                if len(before.channel.members) == 0:
                    for i in before.channel.category.channels:
                        await i.delete()
                    await before.channel.category.delete()

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class AndreeVideos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="randomvideo", aliases=["RandomVideo", "randomVideo", "Randomvideo", "rv", "RV", "rV", "Rv"])
    async def random_video(self, ctx: commands.Context):
        return await ctx.reply(random.choice(videos.videos))
    
    @commands.command(name="paint", aliases=["Paint"])
    async def random_paint(self, ctx: commands.Context):
        return await ctx.reply(random.choice(paints.paints))
    @commands.command(name="members", aliases=["Members", "family", "Family"])
    async def member_count(self, ctx: commands.Context):
        return await ctx.reply(embed=discord.Embed(title="We are currently {} users in the family (Dom would be very proud) :)".format(ctx.guild.member_count), color=discord.Color.from_rgb(255, 255, 255)))

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class NekosAPI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="hug", aliases=["Hug"])
    async def hug_command(self, ctx: commands.Context, member: discord.Member=None):
        if member is None:
            return await ctx.reply(embed=discord.Embed(title="Please @mention someone just right after the command", color=discord.Color.from_rgb(255, 255, 255)))
        try:
            embed = discord.Embed(description="{} hugged {}!!".format(ctx.author.mention, member.mention), color=discord.Color.from_rgb(255, 255, 255))
            embed.set_image(url=nekos.img(target="hug"))
            await ctx.send(embed=embed)

        except:
            return await ctx.reply(embed=discord.Embed(title="Whoops, looks like something went wrong, try again with !slap @mention", color=discord.Color.from_rgb(255, 255, 255)))
    
    @commands.command(name="Slap", aliases=["slap"])
    async def slap_command(self, ctx: commands.Context, member: discord.Member=None):
        if member is None:
            return await ctx.reply(embed=discord.Embed(title="Please @mention someone just right after the command", color=discord.Color.from_rgb(255, 255, 255)))
        try:
            embed = discord.Embed(description="{} slapped {}!!".format(ctx.author.mention, member.mention), color=discord.Color.from_rgb(255, 255, 255))
            embed.set_image(url=nekos.img(target="slap"))
            await ctx.send(embed=embed)

        except:
            return await ctx.reply(embed=discord.Embed(title="Whoops, looks like something went wrong, try again with !slap @mention", color=discord.Color.from_rgb(255, 255, 255)))

    @commands.command(name="Pat", aliases=["pat"])
    async def pat_command(self, ctx: commands.Context, member: discord.Member=None):
        if member is None:
            return await ctx.reply(embed=discord.Embed(title="Please @mention someone just right after the command", color=discord.Color.from_rgb(255, 255, 255)))
        try:
            embed = discord.Embed(description="{} patted {}!!".format(ctx.author.mention, member.mention), color=discord.Color.from_rgb(255, 255, 255))
            embed.set_image(url=nekos.img(target="pat"))
            await ctx.send(embed=embed)

        except:
            return await ctx.reply(embed=discord.Embed(title="Whoops, looks like something went wrong, try again with !slap @mention", color=discord.Color.from_rgb(255, 255, 255)))

    @commands.command(name="kiss", aliases=["Kiss"])
    async def kiss_command(self, ctx: commands.Context, member: discord.Member=None):
        if member is None:
            return await ctx.reply(embed=discord.Embed(title="Please @mention someone just right after the command", color=discord.Color.from_rgb(255, 255, 255)))
        try:
            embed = discord.Embed(description="{} kissed {}!!".format(ctx.author.mention, member.mention), color=discord.Color.from_rgb(255, 255, 255))
            embed.set_image(url=nekos.img(target="kiss"))
            await ctx.send(embed=embed)

        except:
            return await ctx.reply(embed=discord.Embed(title="Whoops, looks like something went wrong, try again with !slap @mention", color=discord.Color.from_rgb(255, 255, 255)))

    @commands.command(name="fact", aliases=["Fact"])
    async def fact_command(self, ctx: commands.Context):
        return await ctx.reply(embed=discord.Embed(title=nekos.fact(), color=discord.Color.from_rgb(255, 255, 255)))
    
    @commands.command(name="wallpaper", aliases=["Wallpaper"])
    async def wallpaper_command(self, ctx: commands.Context):
        if (ctx.channel.id == 0000000000000) or (ctx.channel.id == 0000000000000) or (ctx.channel.id == 0000000000000):
            return await ctx.send(nekos.img(target="wallpaper"))
        else:
            return await ctx.reply(embed=discord.Embed(title="", description="Whoops, looks like you can't use this here. Try using it in <#879178001873502262>", color=discord.Color.from_rgb(255, 255, 255)))
    
    @commands.command(name="avatar", aliases=["Avatar"])
    async def avatar_command(self, ctx: commands.Context):
        return await ctx.send(nekos.img(target="avatar"))
    
    @commands.command(name="Waifu", aliases=["waifu"])
    async def waifu_command(self, ctx: commands.Context):
        return await ctx.send(nekos.img(target="waifu"))
    
    @commands.command(name="Neko", aliases=["neko"])
    async def neko_command(self, ctx: commands.Context):
        return await ctx.send(nekos.img(target="neko"))

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Help_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="Help", aliases=["help"])
    async def help_command(self, ctx):
        await ctx.author.send(embed=discord.Embed(title="Greetings!! I'm Dusto, Andree's server bot :D", description=help.music_help, color=discord.Color.from_rgb(255, 255, 255)))
        await ctx.author.send(embed=discord.Embed(title="", description=help.nekos_api_help, color=discord.Color.from_rgb(255, 255, 255)))
        await ctx.author.send(embed=discord.Embed(title="", description=help.andree_videos_help, color=discord.Color.from_rgb(255, 255, 255)))
        await ctx.author.send(embed=discord.Embed(title="", description=help.temporary_channels_help, color=discord.Color.from_rgb(255, 255, 255)))
    
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

async def setup(client):
    await client.add_cog(Music(client))
    await client.add_cog(DumbCommands(client))
    await client.add_cog(TemporaryVoice(client))
    await client.add_cog(AndreeVideos(client))
    await client.add_cog(NekosAPI(client))
    await client.add_cog(Help_cog(client))
    await client.add_cog(Events(client))
    #await client.add_cog(Sync(client))