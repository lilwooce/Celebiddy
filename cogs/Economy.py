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
        self.baseBeg = 5
        self.minCoinBid = 5
        self.cfMulti = 1
        self.streakLimit = 5
        self.streakAdd = 100

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n----")

    @commands.command()
    @commands.check(hasAccount)
    async def daily(self, ctx):
        userID = ctx.author.id
        user = ctx.author
        rn = datetime.now()
        obj = {"f1": "dailyTimer", "f2": userID}
        checktime = requests.get(getUser, params=obj, headers={"User-Agent": "XY"})
        result = checktime.text.strip('\"')
        result = datetime.strptime(result, "%H:%M:%S")
        if (rn >= result):
            prevTime = result
            next = datetime.now() + timedelta(hours=24)
            next = datetime.strftime(next,"%H:%M:%S")
            balance = requests.get(getUser, params={"f1": "dabloons", "f2": userID}, headers={"User-Agent": "XY"})
            requests.post(updateUser, data={"f1": "dailyTimer", "f2": next, "f3": userID}, headers={"User-Agent": "XY"})
            bal = balance.text.strip('\"')
            streakBuffer = prevTime + timedelta(hours=6)
            print(streakBuffer)
            add = self.baseDaily
            print(rn <= streakBuffer)
            print(rn > streakBuffer)
            if(rn <= streakBuffer):
                streak = requests.get(getUser, params={"f1": "dailyStreak", "f2": userID}, headers={"User-Agent": "XY"})
                s = streak.text.strip('\"')
                if(int(s) < self.streakLimit):
                    add += self.streakAdd * int(s)
                    newS = int(s) + 1
                    requests.post(updateUser, data={"f1": "dailyStreak", "f2": newS, "f3": userID}, headers={"User-Agent": "XY"})
            else:
                requests.post(updateUser, data={"f1": "dailyStreak", "f2": 0, "f3": userID}, headers={"User-Agent": "XY"})
                await ctx.send(f"{user.mention}, your daily streak has been reset")
            r = int(bal) + add
            requests.post(updateUser, data={"f1": "dabloons", "f2": r, "f3": userID}, headers={"User-Agent": "XY"})
            await ctx.channel.send(f"{ctx.author.mention} you recieved {self.baseDaily + (100* int(s))} dabloons, you now have {r} dabloons.")
        else:
            calc = result - rn
            await ctx.channel.send(f"Your daily cooldown is ongoing {ctx.author.mention}, please wait {math.floor(calc.seconds/3600)} hour(s).")
    
    @commands.command(aliases=['w'])
    @commands.check(hasAccount)
    async def work(self, ctx):
        userID = ctx.author.id
        rn = datetime.now()
        checktime = requests.get(getUser, params={"f1": "workTimer", "f2": userID}, headers={"User-Agent": "XY"})
        result = checktime.text.strip('\"')
        result = datetime.strptime(result, "%H:%M:%S")
        if (rn >= result):
            next = datetime.now() + timedelta(hours=6)
            next = datetime.strftime(next,"%H:%M:%S")
            requests.post(updateUser, data={"f1": "workTimer", "f2": next, "f3": userID}, headers={"User-Agent": "XY"})
            balance = requests.get(getUser, params={"f1": "dabloons", "f2": userID}, headers={"User-Agent": "XY"})
            b = balance.text.strip('\"')
            b = int(b) + self.baseWork
            requests.post(updateUser, data={"f1": "dabloons", "f2": b, "f3": userID}, headers={"User-Agent": "XY"})
            await ctx.channel.send(f"{ctx.author.mention} you recieved {self.baseWork} dabloons, you now have {b} dabloons.")
        else:
            calc = result - rn
            await ctx.channel.send(f"Your work cooldown is ongoing {ctx.author.mention}, please wait {math.floor(calc.seconds/3600)} hour(s).")
    
    @commands.command()
    @commands.check(hasAccount)
    async def beg(self, ctx):
        userID = ctx.author.id
        rn = datetime.now()
        checktime = requests.get(getUser, params={"f1": "begTimer", "f2": userID}, headers={"User-Agent": "XY"})
        result = checktime.text.strip('\"')
        result = datetime.strptime(result, "%H:%M:%S")
        if (rn >= result):
            next = datetime.now() + timedelta(minutes=1)
            next = datetime.strftime(next,"%H:%M:%S")
            requests.post(updateUser, data={"f1": "begTimer", "f2": next, "f3": userID}, headers={"User-Agent": "XY"})
            balance = requests.get(getUser, params={"f1": "dabloons", "f2": userID}, headers={"User-Agent": "XY"})
            b = balance.text.strip('\"')
            add = self.baseBeg + random.randint(1, 10)
            b = int(b) + add
            requests.post(updateUser, data={"f1": "dabloons", "f2": b, "f3": userID}, headers={"User-Agent": "XY"})
            await ctx.channel.send(f"{ctx.author.mention} you recieved {add} dabloons, you now have {b} dabloons.")
        else:
            calc = result - rn
            await ctx.channel.send(f"Your beg cooldown is ongoing {ctx.author.mention}, please wait {math.floor(calc.seconds)} second(s).")
        
    @commands.command(aliases=['cf'])
    async def coinflip(self, ctx, bet, amount: int):
        userID = ctx.author.id
        bal = requests.get(getUser, params={"f1": "dabloons", "f2": ctx.author.id}, headers={"User-Agent": "XY"})
        bal = bal.text.strip('\"')
        if(amount <= int(bal)):
            if (amount >= self.minCoinBid):
                bal = requests.get(getUser, params={"f1": "dabloons", "f2": userID}, headers={"User-Agent": "XY"})
                bal = bal.text.strip('\"')
                cBal = int(bal) - amount
                heads = ["heads", "head", "h"]
                tails = ["tails", "tail", "t"]
                result = random.randint(0,1)
                if (result == 0 and bet.lower() in heads):
                    total = amount * (1+self.cfMulti)
                    won = total - amount
                    afterBet = total + cBal
                    requests.post(updateUser, data={"f1": "dabloons", "f2": afterBet, "f3": userID}, headers={"User-Agent": "XY"})
                    await ctx.send(f"Congrats!!! You won {int(won)} dabloons")
                elif (result == 1 and bet.lower() in tails):
                    total = amount * (1+self.cfMulti)
                    won = total - amount
                    afterBet = int(total) + cBal
                    requests.post(updateUser, data={"f1": "dabloons", "f2": afterBet, "f3": userID}, headers={"User-Agent": "XY"})
                    await ctx.send(f"Congrats!!! You won {int(won)} dabloons")
                else:
                    requests.post(updateUser, data={"f1": "dabloons", "f2": int(bal)-amount, "f3": userID}, headers={"User-Agent": "XY"})
                    await ctx.send(f"You lost. lol. -{amount} dabloons")
            else:
                await ctx.send("Bid more money you poor fuck. The minimum bet is 5 dabloons.")
        else:
            await ctx.send("You are too poor to afford this bet. Check your balance before betting next time.")

    @commands.command(aliases=['loan', 'lend'])
    async def give(self, ctx, user: discord.User, amount: int):
        userID = ctx.author.id
        bal = requests.get(getUser, params={"f1": "dabloons", "f2": userID}, headers={"User-Agent": "XY"})
        bal = bal.text.strip('\"')
        if (amount == 0):
            await ctx.send("Why are you trying to give someone nothing? What is wrong with you?")
            return

        if (amount >= 1):
            if(userID != user.id):
                if (amount <= int(bal)):
                    gBal = requests.get(getUser, params={"f1": "dabloons", "f2": user.id}, headers={"User-Agent": "XY"})
                    gBal = gBal.text.strip('\"')
                    requests.post(updateUser, data={"f1": "dabloons", "f2": int(bal)-amount, "f3": userID}, headers={"User-Agent": "XY"})
                    requests.post(updateUser, data={"f1": "dabloons", "f2": int(gBal)+amount, "f3": user.id}, headers={"User-Agent": "XY"})
                    await ctx.send(f"**{ctx.author.name}#{ctx.author.discriminator}** just gave **{amount}** dabloon(s) to **{user.name}#{user.discriminator}**")
                else:
                    await ctx.send("You don't have enough money. Next time don't bite off more than you can chew.")
            else:
                await ctx.send("Are you that lonely that you have to give yourself money? Sad.")
        else:
            await ctx.send("You can't give someone negative dabloons. Are you dumb?")



    
    async def trade(self, ctx):
        return


def setup(bot):
    bot.add_cog(Economy(bot))
