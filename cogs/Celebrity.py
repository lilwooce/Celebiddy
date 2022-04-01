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
getCeleb = os.getenv('GET_CELEB')
addCeleb = os.getenv('ADD_CELEB')


class Celebrity(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n----")
    
    @commands.is_owner()
    @commands.command()
    @commands.guild_only()
    async def mint(self, ctx):
        channel = ctx.channel
        userID = ctx.author.id

        def check(m):
            return m.author.id == userID and m.channel == channel

        await ctx.channel.send("Name: ")
        name = await self.bot.wait_for('message', check=check, timeout=30)
        name = name.content
        await ctx.channel.send("Description: ")
        desc = await self.bot.wait_for('message', check=check, timeout=30)
        desc = desc.content
        await ctx.channel.send("Occupation: ")
        occupation = await self.bot.wait_for('message', check=check, timeout=30)
        occupation = occupation.content
        await ctx.channel.send("Attribute: ")
        attribute = await self.bot.wait_for('message', check=check, timeout=30)
        attribute = attribute.content
        await ctx.channel.send("Series: ")
        series = await self.bot.wait_for('message', check=check, timeout=30)
        series = series.content

        obj = {"f1": name, "f2": desc, "f3": occupation, "f4": attribute, "f5": int(series)}
        await ctx.channel.send(f"You made a celeb with the attributes {obj}")
        r = requests.post(addCeleb, data=obj, headers={"User-Agent": "XY"})
        print(r.text)
        print(r.status_code)

def setup(bot):
    bot.add_cog(Celebrity(bot))
