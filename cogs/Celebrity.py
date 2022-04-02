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
updateCeleb = os.getenv('UPDATE_CELEB')

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
        await ctx.channel.send("Series: ")
        series = await self.bot.wait_for('message', check=check, timeout=30)
        series = series.content
        await ctx.channel.send("Image: ")
        image = await self.bot.wait_for('message', check=check, timeout=30)
        image = image.attachments[0].url

        obj = {"f1": "image", "f2": image, "f3": name, "f4": "series", "f5": int(series)}
        r = requests.post(updateCeleb, data=obj, headers={"User-Agent": "XY"})

def setup(bot):
    bot.add_cog(Celebrity(bot))
