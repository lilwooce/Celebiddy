from ast import alias
from discord.ext import commands
import discord
import math
from datetime import datetime, timedelta
from dotenv import load_dotenv
import requests
import os 

load_dotenv()
getUser = os.getenv('USER_URL')
updateUser = os.getenv('UPDATE_USER')
getCeleb = os.getenv('GET_CELEB')
addCeleb = os.getenv('ADD_CELEB')
updateCeleb = os.getenv('UPDATE_CELEB')
addAuction = os.getenv('ADD_AUCTION')
updateAuction = os.getenv('UPDATE_AUCTION')
getAuction = os.getenv('GET_AUCTION')
removeAuction = os.getenv('REMOVE_AUCTION')
addUser = os.getenv('ADD_USER')

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n----")

    @commands.command(aliases=["am"])
    @commands.is_owner()
    async def addMoney(self, ctx, user, amount: int):
        bal = requests.get(getUser, params={"f1": "dabloons", "f2": user}, headers={"User-Agent": "XY"})
        bal = bal.text.strip('\"')
        requests.post(updateUser, data={"f1": "dabloons", "f2": int(bal)+amount, "f3": user}, headers={"User-Agent": "XY"})
        if (amount < 0) :
            await ctx.send(f"Removed {amount * -1} dabloon(s) from {user}")
        else:
            await ctx.send(f"Added {amount} dabloon(s) to {user}")
    
    @commands.command(aliases=['co'])
    @commands.is_owner()
    async def changeOwnership(self, ctx, owner, *name):
        name = " ".join(name)
        requests.post(updateCeleb, data={"f1": "owner", "f2": owner, "f3": name}, headers={"User-Agent": "XY"})
        await ctx.send(f"Changed the ownership of {name} to {owner}")


def setup(bot):
    bot.add_cog(Admin(bot)) 