import discord
from discord.ext import commands
import asyncio

# a poll button that inherits from discord.ui.Button

voted_player_list = []
author = None

class PollButton(discord.ui.Button):
    message = ''
    count = 1

    # constructor for this poll button.
    def __init__(self, message):
        # calls the super constructor to give the label and style of the button
        super().__init__(label=message, style=discord.ButtonStyle.primary)
        self.message = message

    # defines the behavior after a user clicks a poll button (returns user choice and increments poll)
    async def callback(self, interaction: discord.Interaction):
        # Use the interaction object to send a response message containing
        # the user's choice and increment the poll
        user1 = interaction.user
        if(user1 not in voted_player_list):
            self.count += 1
            voted_player_list.append(user1)
            await interaction.response.send_message(f'{user1.mention}\' has voted {self.message} {self.count} players have voted', ephemeral = False)
        else:
            if(user1 == author):
                await interaction.response.send_message(f'You are already in the game!', ephemeral = True)
            else:
                await interaction.response.send_message(f'You cannot vote twice!', ephemeral = True)

    # poll class that inherits from the discord.ui.View, basically a container for the poll buttons
class Poll(discord.ui.View):

    # constructor for this Poll
    def __init__(self, ctx, timeout):
        # timeout is how many seconds it takes before the on_timeout function runs
        super().__init__(timeout=timeout)
        self.question = 'Do you want to join a current game session?'
        self.ctx = ctx
        args = ['Join Game']
        global voted_player_list
        voted_player_list = []
        global author
        author = ctx.author
        voted_player_list.append(author)
        # creates a poll button for each choice inputted and adds them to the view
        for choice in args:
            self.add_item(PollButton(choice))

    # function runs when this view times out
    async def on_timeout(self):
        # sends the votes for each choice
        for item in self.children:
            await self.ctx.send(f'{item.count} players joined')
            
            if(len(voted_player_list) < 6 or len(voted_player_list) > 12):
                
                await self.ctx.send('Invalid amount of players. The player number cannot be below 6 or above 12')
            else:
                await self.ctx.send('The game starts with' + voted_player_list.size() + 'players')

# cogs let you put related commands and functions together under a class
class Util(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='poll', # brief and description are what show up in the help menu
                    brief='Make a poll that closes in a given amount of seconds',
                    description='Vote on choices!'
                    )
    async def poll(self, ctx: commands.Context, seconds: int):
        '''
        Creates a poll on discord, with the first argument being the question asked, and the following arguments being the choices for the poll
        :param ctx: the character that denotes a command for this bot (?)
        :param mins: the number of seconds before the poll closes
        :return: None
        '''
        view = Poll(ctx,int(seconds))
        await ctx.send('Do you want to join the current game session?', view=view)    
    # add this cog to the client
async def setup(client):
    await client.add_cog(Util(client))
