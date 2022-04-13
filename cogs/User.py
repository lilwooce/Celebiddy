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
header={"User-Agent": "XY"}

class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n----")
    
    @commands.command(aliases=['bal'])
    async def balance(self, ctx, user: discord.User=None):
        if user is None:
            user = ctx.message.author

        checkBalance = requests.get(getUser, params={"f1": "dabloons", "f2": user.id}, headers=header)
        checkBalance = checkBalance.text.strip('\"')

        await ctx.channel.send(f"{user.name}#{user.discriminator} currently has {checkBalance} dabloon(s).")
        
    @commands.command(aliases=['cd'])
    async def cooldowns(self, ctx):
        rn = datetime.now()
        dailyCD = requests.get(getUser, params={"f1": "dailyTimer", "f2": ctx.author.id}, headers=header)
        dailyCD = dailyCD.text.strip('\"')
        dailyCD = datetime.strptime(dailyCD, "%Y-%m-%d %H:%M:%S")
        workCD = requests.get(getUser, params={"f1": "workTimer", "f2": ctx.author.id}, headers=header)
        workCD = workCD.text.strip('\"')
        workCD = datetime.strptime(workCD, "%Y-%m-%d %H:%M:%S")
        begCD = requests.get(getUser, params={"f1": "begTimer", "f2": ctx.author.id}, headers=header)
        begCD = begCD.text.strip('\"')
        begCD = datetime.strptime(begCD, "%Y-%m-%d %H:%M:%S")

        dailyCD = dailyCD - rn
        workCD = workCD - rn
        begCD = begCD - rn

        dailyCD = calcTime(dailyCD)
        workCD = calcTime(workCD)
        begCD = calcTime(begCD)

        embed=discord.Embed(title="Cooldowns", description=f"Showing cooldowns for <@{ctx.author.id}> \n \n **Daily** {dailyCD} \n **Work** {workCD} \n **Beg** {begCD}")
        await ctx.channel.send(embed=embed)
    
    @commands.command(aliases=['v'])
    async def view(self, ctx, *name):
        name = " ".join(name)
        d,o,a,i,owner = await getInfo(ctx, name)
        embed=discord.Embed(title=name, description=f"Works as a(n) {o} \n \n Owned by <@{owner}>", color=discord.Colour.random())
        embed.set_image(url=i)
        if (await isAuction(ctx, name)):
            hUser = requests.get(getAuction, params={"f1": "highestUser", "f2": name}, headers=header)
            hUser = hUser.text.strip("\"")
            hBid = requests.get(getAuction, params={"f1": "highestBid", "f2": name}, headers=header)
            hBid = hBid.text.strip("\"")
            hUser = await self.bot.fetch_user(hUser)
            embed.add_field(name="Highest Bid", value=f"The current highest bid for {name} is {hBid} dabloon(s) by {hUser.mention}")
        await ctx.channel.send(embed=embed)
    
    @commands.command(aliases=['c'])
    async def collection(self, ctx, user: discord.User=None):
        if user is None:
            user = ctx.message.author

        celebs = requests.get(getCeleb, params={"f1": "name", "f2": ctx.author.id, "f3": 'owner'}, headers=header)
        print(celebs.text)
        celebs = celebs.text.strip('\"')
        names = celebs.split(',')
        print(names)
        for name in names:
            n = name.split

def calcTime(time):
    if (time.days < 0):
        return "is available"
    else:
        time = time.seconds
        if(time<3600 and time>60):
            return f"in {math.floor(time/60)} minute(s)"
        elif (time >= 3600):
            return f"in {math.floor(time/3600)} hour(s)"
        else:
            return  f"in {time} second(s)"
        

async def hasAccount(ctx):
    userID = ctx.author.id
    obj = {"f1": "user", "f2": userID}
    result = requests.get(getUser, params=obj, headers=header)
    id = result.text.strip('\"')
    if (id == str(userID)):
        return True
    else:
        await addAccount(ctx)
        return True

async def addAccount(ctx):
    userID = ctx.author.id
    obj = {"f1": userID}
    requests.post(addUser, data=obj, headers=header)

async def exists(ctx, name):
    result = requests.get(getCeleb, params={"f1": "name", "f2": name}, headers=header)
    n = result.text.strip('\"')
    if (name == n):
        return True
    else:
        await ctx.channel.send("This celebrity does not exist in database please add.")
        return False

async def getInfo(ctx, n):
    if (await exists(ctx, n)):
        description = requests.get(getCeleb, params={"f1": "description", "f2": n}, headers=header)
        description = description.text.strip('\"')
        occupation = requests.get(getCeleb, params={"f1": "occupation", "f2": n}, headers=header)
        occupation = occupation.text.strip('\"')
        attribute = requests.get(getCeleb, params={"f1": "attribute", "f2": n}, headers=header)
        attribute = attribute.text.strip('\"')
        owner = requests.get(getCeleb, params={"f1": "owner", "f2": n}, headers=header)
        owner = owner.text.strip('\"')
        image = requests.get(getCeleb, params={"f1": "image", "f2": n}, headers=header)
        image = image.text.replace("\\", "")
        image = image.strip("\"")
        return description,occupation,attribute,image,owner

async def isAuction(ctx, name):
    result = requests.get(getAuction, params={"f1": "celebrity", "f2": name}, headers=header)
    n = result.text.strip('\"')
    if (name == n):
        return True
    else:
        await ctx.channel.send("This celebrity is not currently in auction.")
        return False

def setup(bot):
    bot.add_cog(User(bot))
