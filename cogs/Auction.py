from discord.ext import commands
import discord
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import requests
import os
from .User import hasAccount

load_dotenv()
getUser = os.getenv('USER_URL')
updateUser = os.getenv('UPDATE_USER')
getCeleb = os.getenv('GET_CELEB')
addCeleb = os.getenv('ADD_CELEB')
updateCeleb = os.getenv('UPDATE_CELEB')

class Auction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.picsLink = "http://voiceit2.com/testing/Celebiddy/pics/"
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n----")
    
    @commands.is_owner()
    @commands.command()
    @commands.guild_only()
    async def auction(self, ctx):
        channel = ctx.channel
        userID = ctx.author.id
        
        def check(m):
            return m.author.id == userID and m.channel == channel

        await ctx.channel.send("Name: ")
        name = await self.bot.wait_for('message', check=check, timeout=30)
        name = name.content
        await ctx.channel.send("Series: ")
        series = await self.bot.wait_for('message', check=check, timeout=30)
        series = series.content

        if (await exists(ctx, name, series)):
            localTime = datetime.now(timezone.utc).astimezone().isoformat()
            print(localTime)
            description = requests.get(getCeleb, params={"f1": "description", "f2": name})
            occupation = requests.get(getCeleb, params={"f1": "occupation", "f2": name})
            attribute = requests.get(getCeleb, params={"f1": "attribute", "f2": name})
            embed=discord.Embed(title=name, description="")
            embed.add_field(name="Description", value=description, inline=True)
            embed.add_field(name="Occupation", value=occupation, inline=True)
            embed.add_field(name="Attribute", value=attribute, inline=True)
            embed.set_image(url=f"{self.picsLink}{name}{series}.jpg")
            await ctx.channel.send(embed=embed)

async def exists(ctx, name, series):
    result = requests.get(getCeleb, params={"f1": "name", "f2": name}, headers={"User-Agent": "XY"})
    r = requests.get(getCeleb, params={"f1": "series", "f2": name}, headers={"User-Agent": "XY"})
    n = result.text.strip('\"')
    s = r.text.strip('\"')
    print(f"passed var is {name} type is {type(name)} and database var is {n} type is {type(n)}")
    print(f"passed var is {series} type is {type(series)}  and database var is {s} type is {type(s)}")
    if (name == n and series == s):
        return True
    else:
        await ctx.channel.send("This celebrity does not exist in database please add.")
        return False

def setup(bot):
    bot.add_cog(Auction(bot))
