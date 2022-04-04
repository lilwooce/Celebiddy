from discord.ext import commands
import discord
from discord.ext import tasks
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import requests
import os
import asyncio
from .User import hasAccount

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

class Auction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n----")
    
    @commands.is_owner()
    @commands.command()
    @commands.guild_only()
    async def auction(self, ctx):
        channel = ctx.channel
        rn = datetime.now()
        userID = ctx.author.id
        
        def check(m):
            return m.author.id == userID and m.channel == channel

        await ctx.channel.send("Name: ")
        name = await self.bot.wait_for('message', check=check, timeout=30)
        name = name.content
        await ctx.channel.send("Series: ")
        series = await self.bot.wait_for('message', check=check, timeout=30)
        series = series.content
        await ctx.channel.send("Auction Length: ")
        endTime = await self.bot.wait_for('message', check=check, timeout=30)
        endTime = endTime.content

        d,o,a,i = await getInfo(ctx, name, series)
        embed=discord.Embed(title=name, description="")
        embed.add_field(name="Description", value=d, inline=True)
        embed.add_field(name="Occupation", value=o, inline=True)
        embed.add_field(name="Attribute", value=a, inline=True)
        embed.set_image(url=i)
        await ctx.channel.send(embed=embed)

        requests.post(addAuction, data={"f1": userID, "f2": 0, "f3": userID, "f4": endTime}, headers={"User-Agent": "XY"})
        asyncio.run(await self.stopAuction(ctx, int(endTime), name))

    @commands.command(aliases=["as"])
    async def auctions(self, ctx):
            embed = discord.Embed(title="Auctions", description="")
            current = requests.get(getAuction, params={"f1": "*"}, headers={"User-Agent": "XY"})    
            print(current)
    
    @commands.command()
    async def bid(self, ctx):
        channel = ctx.channel
        rn = datetime.now()
        userID = ctx.author.id
        
        def check(m):
            return m.author.id == userID and m.channel == channel

        await ctx.channel.send("Celebrity Name: ")
        name = await self.bot.wait_for('message', check=check, timeout=30)
        name = name.content
        await ctx.channel.send("Amount: ")
        amount = await self.bot.wait_for('message', check=check, timeout=30)
        amount = amount.content

        if (await isAuction(ctx, name)):
            requests.post(updateAuction, data={"f1": "highestBid", "f2": amount, "f3": name}, headers={"User-Agent": "XY"})
            requests.post(updateAuction, data={"f1": "highestUser", "f2": userID, "f3": name}, headers={"User-Agent": "XY"})
            await ctx.send(f"You bid {amount} dabloon(s) on {name}")

    async def stopAuction(self, ctx, time, name):
        await asyncio.sleep(time*3600)
        winner = requests.get(getAuction, params={"f1": "highestUser", "f2": name}, headers={"User-Agent": "XY"})
        winner = winner.text.strip("\"")
        amount = requests.get(getAuction, params={"f1": "highestBid", "f2": name}, headers={"User-Agent": "XY"})
        amount = amount.text.strip("\"")
        requests.post(removeAuction, data={"f1": name}, headers={"User-Agent": "XY"})
        requests.post(updateCeleb, data={"f1": "owner", "f2": winner, "f3": name}, headers={"User-Agent": "XY"})
        user = self.bot.get_user(winner)
        await user.send(f"Congrats! You won the auction for {name} with {amount} dabloons")


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

async def isAuction(ctx, name):
    result = requests.get(getAuction, params={"f1": "celebrity", "f2": name}, headers={"User-Agent": "XY"})
    auctioneer = requests.get(getAuction, params={"f1": "auctioneer", "f2": name}, headers={"User-Agent": "XY"})
    n = result.text.strip('\"')
    auctioneer = auctioneer.text.strip('\"')
    if (name == n and auctioneer == ctx.author.id):
        return True
    else:
        await ctx.channel.send("This celebrity is not currently in auction.")
        return False

async def getInfo(ctx, n, s):
    if (await exists(ctx, n, s)):
        description = requests.get(getCeleb, params={"f1": "description", "f2": n}, headers={"User-Agent": "XY"})
        print(f"status code is {description.status_code}")
        description = description.text.strip('\"')
        occupation = requests.get(getCeleb, params={"f1": "occupation", "f2": n}, headers={"User-Agent": "XY"})
        occupation = occupation.text.strip('\"')
        attribute = requests.get(getCeleb, params={"f1": "attribute", "f2": n}, headers={"User-Agent": "XY"})
        attribute = attribute.text.strip('\"')
        image = requests.get(getCeleb, params={"f1": "image", "f2": n}, headers={"User-Agent": "XY"})
        image = image.text.replace("\\", "")
        image = image.strip("\"")
        print(image)
        return description,occupation,attribute,image

def setup(bot):
    bot.add_cog(Auction(bot))
