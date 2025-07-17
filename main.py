import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix="%", intents=intents)

@client.event
async def on_ready():
    await client.load_extension("dustobot")
    await client.change_presence(status=discord.Status.online, activity=discord.Game("%help"))

client.remove_command("help") #I have my own help command     

if __name__ == "__main__":
    client.run(TOKEN)