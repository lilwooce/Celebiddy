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
        if(begCD.seconds >= 61):
            begCD = "is available"
        else:
            begCD = calcTime(begCD.seconds)

        embed=discord.Embed(title="Cooldowns", description=f"**Daily** {dailyCD} \n **Work** {workCD} \n **Beg** {begCD}")
        await ctx.channel.send(embed=embed)
    
    @commands.command(aliases=['v'])
    async def view(self, ctx, series=1, *name):
        for x in name:
            name += x + " "
        d,o,a,i,owner = await getInfo(ctx, name, series)
        embed=discord.Embed(title=name, description=f"Works as a(n) {o} \n Owned by <@{owner}>", color=discord.Colour.random())
        embed.add_field(name="Occupation", value=o, inline=True)
        embed.set_image(url=i)
        await ctx.channel.send(embed=embed)

def calcTime(time):
    if(time<3600 and time>60):
        return f"in {math.floor(time/60)} minute(s)"
    elif (time >= 3600):
        return f"in {math.floor(time/3600)} hour(s)"
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

async def exists(ctx, name, series):
    result = requests.get(getCeleb, params={"f1": "name", "f2": name}, headers={"User-Agent": "XY"})
    r = requests.get(getCeleb, params={"f1": "series", "f2": name}, headers={"User-Agent": "XY"})
    n = result.text.strip('\"')
    s = r.text.strip('\"')
    if (name == n and series == s):
        return True
    else:
        await ctx.channel.send("This celebrity does not exist in database please add.")
        return False

async def getInfo(ctx, n, s):
    if (await exists(ctx, n, s)):
        print(n)
        print(s)
        description = requests.get(getCeleb, params={"f1": "description", "f2": n}, headers={"User-Agent": "XY"})
        print(f"status code is {description.status_code}")
        description = description.text.strip('\"')
        occupation = requests.get(getCeleb, params={"f1": "occupation", "f2": n}, headers={"User-Agent": "XY"})
        occupation = occupation.text.strip('\"')
        attribute = requests.get(getCeleb, params={"f1": "attribute", "f2": n}, headers={"User-Agent": "XY"})
        attribute = attribute.text.strip('\"')
        owner = requests.get(getCeleb, params={"f1": "owner", "f2": n}, headers={"User-Agent": "XY"})
        owner = owner.text.strip('\"')
        image = requests.get(getCeleb, params={"f1": "image", "f2": n}, headers={"User-Agent": "XY"})
        image = image.text.replace("\\", "")
        image = image.strip("\"")
        return description,occupation,attribute,image,owner

def setup(bot):
    bot.add_cog(User(bot))
