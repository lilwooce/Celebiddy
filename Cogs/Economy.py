from discord.ext import commands
import discord
from datetime import datetime, timedelta
from dotenv import load_dotenv
import requests
import os 
from cogs.User import hasAccount

load_dotenv()
getUser = os.getenv('USER_URL')

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n----")

    @commands.Cog.listener()
    @commands.check(hasAccount)
    async def daily(self):
        return

def setup(bot):
    bot.add_cog(Economy(bot))