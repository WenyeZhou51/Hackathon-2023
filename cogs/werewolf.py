import discord
from discord.ext import commands
import asyncio


# Inputs: players who are assigned wolf role
class Werewolf(commands.Cog):
    werewolves = []
    responses = []

    def __init__(self, werewolves):
        self.werewolves = werewolves
    
    def collect_responses(self):
        for werewolf in self.werewolves:
            self.responses.append() #DM_poll_function

    def determine_dead_player(self):
        if (len(self.responses) % 2):

if 0:
    print('hey')

        

