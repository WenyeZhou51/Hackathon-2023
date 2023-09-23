
import discord
from discord.ext import commands
import asyncio

class werewolf(commands.Cog):
    def __init__(self, client):
        self.client = client

async def setup(client):
    await client.add_cog(Util(client))