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
addUser = os.getenv('ADD_USER')

class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n----")
    
    @commands.command(aliases=['bal'])
    async def balance(self, ctx):
        checkBalance = requests.get(getUser, params={"f1": "dabloons", "f2": ctx.author.id}, headers={"User-Agent": "XY"})
        checkBalance = checkBalance.text.strip('\"')
        await ctx.channel.send(f"{ctx.author.mention} you currently have {checkBalance} dabloon(s).")
        
    @commands.command(aliases=['cd'])
    async def cooldowns(self, ctx):
        rn = datetime.now()
        dailyCD = requests.get(getUser, params={"f1": "dailyTimer", "f2": ctx.author.id}, headers={"User-Agent": "XY"})
        dailyCD = dailyCD.text.strip('\"')
        dailyCD = dailyCD[:-7]
        dailyCD = datetime.strptime(dailyCD, "%Y-%m-%d %H:%M:%S")
        workCD = requests.get(getUser, params={"f1": "workTimer", "f2": ctx.author.id}, headers={"User-Agent": "XY"})
        workCD = workCD.text.strip('\"')
        workCD = workCD[:-7]
        workCD = datetime.strptime(workCD, "%Y-%m-%d %H:%M:%S")
        begCD = requests.get(getUser, params={"f1": "begTimer", "f2": ctx.author.id}, headers={"User-Agent": "XY"})
        begCD = begCD.text.strip('\"')
        begCD = begCD[:-7]
        begCD = datetime.strptime(begCD, "%Y-%m-%d %H:%M:%S")

        dailyCD = dailyCD - rn
        workCD = workCD - rn
        begCD = begCD - rn

        dailyCD = calcTime(dailyCD.seconds)
        workCD = calcTime(workCD.seconds)
        begCD = calcTime(begCD.seconds)
        
        embed=discord.embed(title="Cooldowns", description=f"**Daily** {dailyCD} \n **Work** {workCD} \n **Beg** {begCD}")
        await ctx.channel.send(embed=embed)

def calcTime(time):
    if(time<3600 and time>60):
        return f"in {time/60} minute(s)"
    elif (time >= 3600):
        return f"in {time/3600} hour(s)"
    elif (time <=0):
        return "is available"
    else:
        return  f"in {time} second(s)"

async def hasAccount(ctx):
    userID = ctx.author.id
    obj = {"f1": "user", "f2": userID}
    result = requests.get(getUser, params=obj, headers={"User-Agent": "XY"})
    id = result.text.strip('\"')
    if (id == str(userID)):
        return True
    else:
        await addAccount(ctx)
        return True

async def addAccount(ctx):
    userID = ctx.author.id
    obj = {"f1": userID}
    requests.post(addUser, data=obj, headers={"User-Agent": "XY"})

def setup(bot):
    bot.add_cog(User(bot))
