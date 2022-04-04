from discord.ext import commands
import discord
from datetime import datetime, timedelta
from dotenv import load_dotenv
import requests
import math
import random
import os
from .User import hasAccount

load_dotenv()
getUser = os.getenv('USER_URL')
updateUser = os.getenv('UPDATE_USER')
getCeleb = os.getenv('GET_CELEB')
addCeleb = os.getenv('ADD_CELEB')
updateCeleb = os.getenv('UPDATE_CELEB')

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.baseDaily = 500
        self.baseWork = 1000

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n----")

    @commands.command()
    @commands.check(hasAccount)
    async def daily(self, ctx):
        userID = ctx.author.id
        rn = datetime.now()
        obj = {"f1": "dailyTimer", "f2": userID}
        checktime = requests.get(getUser, params=obj, headers={"User-Agent": "XY"})
        result = checktime.text.strip('\"')
        result = result[:-7]
        result = datetime.strptime(result, "%Y-%m-%d %H:%M:%S")
        if (rn >= result):
            balance = requests.get(getUser, params={"f1": "dabloons", "f2": userID}, headers={"User-Agent": "XY"})
            streak = requests.get(getUser, params={"f1": "dailyStreak", "f2": userID}, headers={"User-Agent": "XY"})
            r = balance.text.strip('\"')
            s = streak.text.strip('\"')
            r = int(r) + self.baseDaily + (100 * int(s))
            requests.post(updateUser, data={"f1": "dabloons", "f2": r, "f3": userID}, headers={"User-Agent": "XY"})
            await ctx.channel.send(f"You recieved {self.baseDaily + (100* int(s))} dabloons, you now have {r} dabloons.")
            next = datetime.now() + timedelta(hours=24)
            requests.post(updateUser, data={"f1": "dailyTimer", "f2": next, "f3": userID}, headers={"User-Agent": "XY"})
            requests.post(updateUser, data={"f1": "dailyStreak", "f2": int(s) + 1, "f3": userID}, headers={"User-Agent": "XY"})
        else:
            calc = result - rn
            await ctx.channel.send(f"Your daily cooldown in ongoing, please wait {math.floor(calc.seconds/3600)} hour(s).")
    
    @commands.command(aliases=['w'])
    @commands.check(hasAccount)
    async def work(self, ctx):
        userID = ctx.author.id
        rn = datetime.now()
        checktime = requests.get(getUser, params={"f1": "workTimer", "f2": userID}, headers={"User-Agent": "XY"})
        result = checktime.text.strip('\"')
        result = result[:-7]
        result = datetime.strptime(result, "%Y-%m-%d %H:%M:%S")
        if (rn >= result):
            balance = requests.get(getUser, params={"f1": "dabloons", "f2": userID}, headers={"User-Agent": "XY"})
            b = balance.text.strip('\"')
            b = int(b) + self.baseWork
            requests.post(updateUser, data={"f1": "dabloons", "f2": b, "f3": userID}, headers={"User-Agent": "XY"})
            await ctx.channel.send(f"You recieved {self.baseWork} dabloons, you now have {b} dabloons.")
            next = datetime.now() + timedelta(hours=6)
            requests.post(updateUser, data={"f1": "workTimer", "f2": next, "f3": userID}, headers={"User-Agent": "XY"})
        else:
            calc = result - rn
            await ctx.channel.send(f"Your work cooldown in ongoing, please wait {math.floor(calc.seconds/3600)} hour(s).")
    
    @commands.command(aliases=['b'])
    @commands.check(hasAccount)
    async def beg(self, ctx):
        userID = ctx.author.id
        rn = datetime.now()
        checktime = requests.get(getUser, params={"f1": "begTimer", "f2": userID}, headers={"User-Agent": "XY"})
        result = checktime.text.strip('\"')
        result = result[:-7]
        result = datetime.strptime(result, "%Y-%m-%d %H:%M:%S")
        if (rn >= result):
            balance = requests.get(getUser, params={"f1": "dabloons", "f2": userID}, headers={"User-Agent": "XY"})
            b = balance.text.strip('\"')
            add = self.baseBeg + random.randint(10, 20)
            b = int(b) + add
            requests.post(updateUser, data={"f1": "dabloons", "f2": b, "f3": userID}, headers={"User-Agent": "XY"})
            await ctx.channel.send(f"You recieved {add} dabloons, you now have {b} dabloons.")
            next = datetime.now() + timedelta(minutes=5)
            requests.post(updateUser, data={"f1": "begTimer", "f2": next, "f3": userID}, headers={"User-Agent": "XY"})
        else:
            calc = result - rn
            await ctx.channel.send(f"Your beg cooldown in ongoing, please wait {math.floor(calc.seconds/60)} minutes(s).")


def setup(bot):
    bot.add_cog(Economy(bot))
