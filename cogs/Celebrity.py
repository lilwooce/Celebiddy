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
        await ctx.channel.send("Description: ")
        desc = await self.bot.wait_for('message', check=check, timeout=30)
        await ctx.channel.send("Occupation: ")
        occupation = await self.bot.wait_for('message', check=check, timeout=30)
        await ctx.channel.send("Attribute: ")
        attribute = await self.bot.wait_for('message', check=check, timeout=30)
        await ctx.channel.send("Series: ")
        series = await self.bot.wait_for('message', check=check, timeout=30)

        r = requests.post(addCeleb, data={"f1": name, "f2": desc, "f3": occupation, "f4": attribute, "f5": series}, headers={"User-Agent": "XY"})
        print(r.status_code)

def setup(bot):
    bot.add_cog(Celebrity(bot))
