from discord.ext import commands
import discord
from datetime import datetime, timedelta
from dotenv import load_dotenv
import requests
import os 

load_dotenv()
getUser = os.getenv('USER_URL')
addUser = os.getenv('ADD_USER')

class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n----")

async def hasAccount(ctx):
    userID = ctx.author.id
    obj = {"f1": "user", "f2": userID}
    result = requests.get(getUser, params=obj, headers={"User-Agent": "XY"})
    id = result.text.strip('\"')
    print(f"id variable is type {type(id)}")
    print(f"userID variable is type {type(userID)}")
    if (id == userID):
        return True
    else:
        await addAccount(ctx)
        await ctx.channel.send("No account found... creating")
        return False

async def addAccount(ctx):
    userID = ctx.author.id
    obj = {"f1": userID}
    result = requests.post(addUser, data=obj, headers={"User-Agent": "XY"})
    print(f"add account requests completed with a status code of {result.status_code}")

def setup(bot):
    bot.add_cog(User(bot))