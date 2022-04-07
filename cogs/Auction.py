from discord.ext import commands
import discord
from discord.ext import tasks
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import requests
import os
import random
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

        d,o,a,i,owner = await getInfo(ctx, name, series)
        embed=discord.Embed(title=name, description="", color=discord.Colour.random())
        embed.add_field(name="Occupation", value=o, inline=True)
        embed.set_image(url=i)
        await ctx.channel.send(embed=embed)
        requests.post(addAuction, data={"f1": userID, "f2": name, "f3": 0, "f4": userID}, headers={"User-Agent": "XY"})
        await self.stopAuction(ctx, int(endTime), name, embed)
            

    '''@commands.command(aliases=["as"])
    async def auctions(self, ctx):
            embed = discord.Embed(title="Auctions", description="")
            current = requests.get(getAuction, params={"f1": "*"}, headers={"User-Agent": "XY"})    
            print(current.text[0])
            print(current.text)'''
    
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
            hb = requests.get(getAuction, params={"f1": "highestBid", "f2": name}, headers={"User-Agent": "XY"})
            bal = requests.get(getUser, params={"f1": "dabloons", "f2": ctx.author.id}, headers={"User-Agent": "XY"})
            hb = hb.text.strip('\"')
            bal = bal.text.strip('\"')
            if(int(amount) <= int(bal)):  
                if (int(amount) > int(hb)):
                    requests.post(updateAuction, data={"f1": "highestBid", "f2": amount, "f3": name}, headers={"User-Agent": "XY"})
                    requests.post(updateAuction, data={"f1": "highestUser", "f2": userID, "f3": name}, headers={"User-Agent": "XY"})
                    await ctx.send(f"You bid {amount} dabloon(s) on {name}")
                else:
                    await ctx.send(f"The current highest bid is {hb}. Bid higher loser.")
            else:
                await ctx.send("You are too poor to afford this bid. Check your balance before bidding next time.")

    async def stopAuction(self, ctx, time, name, embed):
        updateChannel = self.bot.get_channel(960595719704678451)
        msg = await updateChannel.send(f"{name}'s auction is starting now, it ends in {time} hour(s). Good Luck!", embed=embed)
        await msg.publish()
        await asyncio.sleep(time*3600)
        winner = requests.get(getAuction, params={"f1": "highestUser", "f2": name}, headers={"User-Agent": "XY"})
        winner = winner.text.strip("\"")
        amount = requests.get(getAuction, params={"f1": "highestBid", "f2": name}, headers={"User-Agent": "XY"})
        amount = amount.text.strip("\"")
        balance = requests.get(getUser, params={"f1": "dabloons", "f2": winner}, headers={"User-Agent": "XY"})
        balance = balance.text.strip("\"")
        requests.post(removeAuction, data={"f1": name}, headers={"User-Agent": "XY"})
        requests.post(updateUser, data={"f1": "dabloons", "f2": int(balance)-int(amount), "f3": winner}, headers={"User-Agent": "XY"})
        requests.post(updateCeleb, data={"f1": "owner", "f2": winner, "f3": name}, headers={"User-Agent": "XY"})
        user = await self.bot.fetch_user(winner)
        await user.send(f"Congrats! You won the auction for {name} with {amount} dabloon(s)")
        msg = await updateChannel.send(f"{name}'s auction is starting now, it ends in {time} hour(s). Good Luck!", embed=embed)
        await msg.publish(f"{user.name}#{user.discriminator} won the auction for {name} with {amount} dabloons. Congrats!")

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
    n = result.text.strip('\"')
    if (name == n):
        return True
    else:
        await ctx.channel.send("This celebrity is not currently in auction.")
        return False

'''async def isOwner(ctx, name):
    result = requests.get(getCeleb, params={"f1": "name", "f2": name}, headers={"User-Agent": "XY"})
    n = result.text.strip('\"')
    result = requests.get(getCeleb, params={"f1": "owner", "f2": name}, headers={"User-Agent": "XY"})
    o = result.text.strip('\"')
    if (name == n and ctx.author.id == int(o)):
        return True
    else:
        await ctx.channel.send("You do not own this Celebrity.")
        return False'''

async def getInfo(ctx, n, s):
    if (await exists(ctx, n, s)):
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
    bot.add_cog(Auction(bot))
