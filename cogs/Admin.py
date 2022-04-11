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
        print(owner)
        print(name)
        requests.post(updateCeleb, data={"f1": "owner", "f2": owner, "f3": name}, headers={"User-Agent": "XY"})
        await ctx.send(f"Changed the ownership of {name} to {owner}")
    
    @commands.command(aliases=['rcd'])
    @commands.is_owner()
    async def resetCooldowns(self, ctx, user: discord.User):
        userID = user.id
        rTime = datetime.now()
        rTime = datetime.strftime(rTime,"%H:%M:%S")
        requests.post(updateUser, data={"f1": "dailyTimer", "f2": rTime, "f3": userID}, headers={"User-Agent": "XY"})
        requests.post(updateUser, data={"f1": "workTimer", "f2": rTime, "f3": userID}, headers={"User-Agent": "XY"})
        requests.post(updateUser, data={"f1": "begTimer", "f2": rTime, "f3": userID}, headers={"User-Agent": "XY"})
    
    @commands.command(aliases=['ccd'])
    @commands.is_owner()
    async def changeCooldowns(self, ctx, user: discord.User, amount: int):
        userID = user.id
        dailyCD = requests.get(getUser, params={"f1": "dailyTimer", "f2": ctx.author.id}, headers={"User-Agent": "XY"})
        dailyCD = dailyCD.text.strip('\"')
        dailyCD = datetime.strptime(dailyCD, "%H:%M:%S")
        requests.post(updateUser, data={"f1": "dailyTimer", "f2": dailyCD + timedelta(hours=amount), "f3": userID}, headers={"User-Agent": "XY"})

def setup(bot):
    bot.add_cog(Admin(bot)) 