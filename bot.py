import discord
from dotenv import load_dotenv
from discord.ext import commands
import os
import traceback
import requests
import sys

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
getPrefix = os.getenv('GET_PREFIX')
addPrefix = os.getenv('ADD_PREFIX')
updatePrefix = os.getenv('UPDATE_PREFIX')
removePrefix = os.getenv('REMOVE_PREFIX')
intents = discord.Intents.default()
intents.members = True

def get_prefix(client, message):
    obj = {"f1": message.guild.id}
    result = requests.get(getPrefix, params=obj, headers={"User-Agent": "XY"})
    print(result)
    prefix = result.text.strip('\"')
    print(prefix)
    return prefix

bot = commands.Bot(command_prefix=[getPrefix], intents=intents, description="Bid on and collect your favorite celebs.")

@bot.event
async def on_ready():
    print(f'{bot.user} has connected')
    activity = discord.Game(name="Celebrity Auction Simulator")
    await bot.change_presence(status=discord.Status.online, activity=activity)

@bot.event
async def on_guild_join(guild):
    obj = {"f1": guild.id, "f2": 'b'}
    result = requests.post(addPrefix, data=obj, headers={"User-Agent": "XY"})
    print(result.text)
    print(result.status_code)

@bot.event
async def on_guild_remove(guild):
    obj = {"q1": guild.id}
    result = requests.post(removePrefix, data=obj, headers={"User-Agent": "XY"})
    print(result.status_code)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        try:
            bot.load_extension(f'cogs.{filename[:-3]}')
        except Exception as e:
            print(f'Failed to load extension cogs.{filename[:-3]}.', file=sys.stderr)
            traceback.print_exc()

bot.run(token)