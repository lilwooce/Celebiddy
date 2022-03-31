from discord.ext import commands
import discord
from datetime import datetime, timedelta
from dotenv import load_dotenv
import requests
import os
from .User import hasAccount

load_dotenv()
getUser = os.getenv('USER_URL')
updateUser = os.getenv('UPDATE_USER')

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.baseDaily = 500

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n----")

    @commands.command()
    @commands.check(hasAccount)
    async def daily(self, ctx):
        print("daily check completed")
        userID = ctx.author.id
        rn = datetime.now()
        obj = {"f1": "dailyTimer", "f2": userID}
        checktime = requests.get(getUser, params=obj, headers={"User-Agent": "XY"})
        result = checktime.text.strip('\"')
        result = result[:-7]
        result = datetime.strptime(result, "%Y-%m-%d %H:%M:%S")
        if (rn >= result):
            balance = requests.get(getUser, params={"f1": "dabloons", "f2": userID}, headers={"User-Agent": "XY"})
            r = balance.text.strip('\"')
            r = int(r) + self.baseDaily
            requests.post(updateUser, data={"f1": "dabloons", "f2": r, "f3": userID}, headers={"User-Agent": "XY"})
            await ctx.channel.send(f"You recieved {self.baseDaily} dabloons, you now have {r} dabloons.")
            next = datetime.now() + timedelta(hours=24)
            requests.post(updateUser, data={"f1": "dailyTimer", "f2": next, "f3": userID}, headers={"User-Agent": "XY"})
        else:
            calc = rn - result
            print(calc)
            await ctx.channel.send(f"Your daily cooldown in ongoing, please wait  hour(s).")

def setup(bot):
    bot.add_cog(Economy(bot))
