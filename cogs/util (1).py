import discord
from discord.ext import commands
import asyncio
import random
from collections import Counter
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
    def __init__(self, ctx, timeout, client):
        # timeout is how many seconds it takes before the on_timeout function runs
        super().__init__(timeout=timeout)
        self.client = client
        args = ['Join Game']
        global author
        author = ctx.author
        self.ctx = ctx
        global voted_player_list
        voted_player_list = []
        voted_player_list.append(author)
        # creates a poll button for each choice inputted and adds them to the view
        for choice in args:
            self.add_item(PollButton(choice))

    # function runs when this view times out
    async def on_timeout(self):
        # sends the votes for each choice
        for item in self.children:
            await self.ctx.send(f'{item.count} players joined')

            start_game = True

            if(len(voted_player_list) < 6 or len(voted_player_list) > 12):       
                await self.ctx.send('Invalid amount of players. The player number cannot be below 6 or above 12')
                start_game = False
            else:
                await self.ctx.send('The game starts with ' + str(len(voted_player_list)) + ' players')
            
            if(start_game):
                player_num = len(voted_player_list)
                player_role_list = []
                player_status = []
                player_name = {}

                for i in range(player_num):
                    player_role_list.append(0)
                    player_status.append(1)
                    player_name[i] = [voted_player_list[i], None]
                
                player_role_list, player_name = await allocatingroles(player_num, player_role_list, player_name, self.client)
                await Game(player_num, player_role_list, player_name, player_status, self.ctx, self.client)

# cogs let you put related commands and functions together under a class

selected = []
voters = []
general_meeting = False

class GPPollButton(discord.ui.Button):
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
        global selected
        if(general_meeting):
            if(user1 not in voted_player_list):
                self.count += 1
                voted_player_list.append(user1)
                selected.append(self.message)
                await interaction.response.send_message(f'You have voted {self.message}', ephemeral = True)
            
            else:
                await interaction.response.send_message(f'You cannot vote twice!', ephemeral = True)
        else:
            if(user1 in voters):
                selected.append([user1, self.message])
                await interaction.response.send_message(f'You have voted {self.message}, feel free to change your vote in the time limit', ephemeral = True)
            else:
                await interaction.response.send_message(f'You are not supposed to vote this round', ephemeral = True)

class GPPoll(discord.ui.View):
    
    # constructor for this Poll
    def __init__(self, ctx, timeout, client, players):
        # timeout is how many seconds it takes before the on_timeout function runs
        super().__init__(timeout=timeout)
        self.ctx = ctx
        self.client = client
        global voted_player_list
        voted_player_list = []

        # creates a poll button for each choice inputted and adds them to the view
        for choice in players:
            self.add_item(GPPollButton(choice))
    
    async def on_timeout(self):
        # sends the votes for each choice
        await self.ctx.send('Vote ended')


async def allocatingroles(player_num, player, player_names, client):
    roles = {1: 'villager', 2: 'werewolf', 3: 'seer', 4: 'witch', 5: 'hunter',
         6: 'guard'}
    villager_num = 4
    werewolf_num = 4
    if(player_num == 11):
        villager_num -= 1
    elif(player_num == 10):
        werewolf_num -= 1
    elif(player_num == 9):
        werewolf_num -= 1
        villager_num -= 1
    elif(player_num == 8):
        werewolf_num -= 1
        villager_num -= 2
    elif(player_num == 7):
        werewolf_num -= 2
        villager_num -= 1
    elif(player_num == 6):
        werewolf_num -= 2
        villager_num -= 2
    count = 0
    rolenum = 1
    while(count < player_num):
        num = random.randint(0, player_num - 1)
        if(player[num] != 0):
            continue
        if(player[num] == 0):
            player[num] = rolenum
            message = 'You are a ' + str(roles[rolenum])
            user = await client.fetch_user(player_names[num][0].id)
            await user.send(message)
            player_names[num][1] = roles[rolenum]
            count += 1
            if(rolenum >= 3):
                rolenum += 1
                continue
            if(count == villager_num and rolenum == 1):
                rolenum += 1
            if(count == villager_num + werewolf_num and rolenum == 2):
                rolenum += 1
    return player, player_names     

class witch():
    def __init__(self, player):
        self.id = player
        self.medicine = 1
        self.poison = 1

def check_game_end(player_role_list):
    # num of bad guys >= num of good guys
    # num of bad guys = 0
    num_werewolves = 0
    num_others = 0
    for role in player_role_list:
        if role == 2:
            num_werewolves += 1
        else:
            num_others += 1
        
    return num_werewolves >= num_others or num_werewolves == 0

async def hunter(shoot, player_role_list, player_name, ctx, client):
    if(shoot):
            
        player_list = list(player_name.values())
        global voters
        voters = []

        for i in range(len(player_list)):
            if(player_list[i][1] == 'hunter'):
                voters.append(player_list[i][0])
                break

        player_name_list = []

        for i in range(len(player_list)):
            player_name_list.append(player_list[i][0].name)
        
        selected = []
        
        view = GPPoll(ctx, 15, client, player_name_list)
        await ctx.send('The hunter is taking down someone with him!', view=view)
        await asyncio.sleep(15)

        if(len(selected) > 0):
            deathh = selected.pop()
            await ctx.send('The hunter shot' + str(deathh) + ' and they died! How terrible!')
            for key1, value1 in player_name.items():
                if value1 == deathh:
                    position1 = key1
            player_name.pop(position1)
            player_role_list.pop(position1)
        return player_name, player_role_list

async def Game(player_num, player_role_list, player_name, player_status, ctx, client):
    round = 1
    player_witch = None
    while(check_game_end(player_role_list) == False):
        await ctx.send('It is now night time!')

        death = None
        death_w = None
        global selected
        selected = []
        if(player_num >= 11):
            if(round == 1):
                global pre_selected
                pre_selected = None
            await ctx.send("It is the guard's turn!")
            await ctx.send('You can defend a player tonight!')

            player_list = list(player_name.values())
            vote_list = []

            for i in range(len(player_list)):
                if(player_list[i][1] == 'guard'):
                    vote_list.append(player_list[i][1])

            player_name_list = []

            for i in range(len(player_list)):
                if(pre_selected == player_list[i][0]):
                    continue
                player_name_list.append(player_list[i][0])
                    

            view = GPPoll(ctx, 15, client, player_name_list)
            await ctx.send('Who do you want to defend tonight?', view=view)
            
            pre_selected = selected.pop()
            selected = [pre_selected]
        
        await ctx.send("It is the werewolf's turn!")
        await ctx.send("You can kill a person tonight!")

        player_list = list(player_name.values())
        global voters
        voters = []

        for i in range(len(player_list)):
            if(player_list[i][1] == 'werewolf'):
                voters.append(player_list[i][0])
            
        player_name_list = []

        for i in range(len(player_list)):
            player_name_list.append(player_list[i][0].name)
            
        selected = []
        
        view = GPPoll(ctx, 30, client, player_name_list)
        await ctx.send('Who do you want to kill tonight?', view=view)

        await asyncio.sleep(30)

        target_list = []
        count = 0
        if(len(selected) > 0):
            last = selected.pop()
            target_list.append(last[1])
            temp_player = last[0]
            voters.remove(temp_player)
            count = len(selected) - 1

            while(count >= 0 and len(voters) > 0):
                if(selected[count][0] != temp_player):
                    target_list.append(selected[count][1])
                    temp_player = selected[count][0]
                    voters.remove(temp_player)
                count -= 1
        
        death = max(target_list, key = target_list.count)

        await ctx.send("It is the witch's turn!")

        player_list = list(player_name.values())
        voters = []

        for i in range(len(player_list)):
            if(player_list[i][1] == 'witch'):
                voters.append(player_list[i][0])
                break
        
        if(round == 1):
            player_witch = witch(voters[0])

        player_name_list = []

        for i in range(len(player_list)):
            player_name_list.append(player_list[i][0].name)
            
        selected = []
        
        if(player_witch.medicine == 1):
            view = GPPoll(ctx, 30, client, ['Yes', 'No'])
            await ctx.send('A person died tonight, are you going to save them', view=view)
            await asyncio.sleep(30)
            if(death != None and (len(selected) == 0 or selected[0][1] == 'Yes')):
                death = None
                player_witch.medicine -= 1
        else:
            await ctx.send('A person died tonight, are you going to save them')
            await asyncio.sleep(30)

        selected = []
        if(player_witch.poison == 1):
            view = GPPoll(ctx, 30, client, player_name_list)
            await ctx.send('Do you want to use your poison on anyone', view=view)
            await asyncio.sleep(30)
            if(len(selected) > 0):
                death_w = selected.pop()
            player_witch.poison -= 1
        else:
            await ctx.send('Do you want to use your poison on anyone')
            await asyncio.sleep(30)
        await ctx.send("It is the seer's turn!")

        player_list = list(player_name.values())
        player_num_list = list(player_name.keys())
        voters = []

        for i in range(len(player_list)):
            if(player_list[i][1] == 'seer'):
                voters.append(player_list[i][0])
                break

        player_name_list = []

        for i in range(len(player_list)):
            player_name_list.append(player_list[i][0].name)
            
        selected = []
        
        view = GPPoll(ctx, 30, client, player_name_list)
        await ctx.send('Select the person you want to check on tonight', view=view)
        await asyncio.sleep(30)
        

        if(len(selected) > 0):
            person = selected.pop()
            index = 0
            for i in player_num_list:
                if(player_name[i][0].name == person[1]):
                    index = i + 1
                    break
            if(player_name[index][1] != 'werewolf'):
                message = 'The person you are checking is a good person'
                user = await client.fetch_user(player_name[index][0].id)
                await user.send(message)
            else:
                message = 'The person you are checking is a bad person'
                user = await client.fetch_user(player_name[index][0].id)
                await user.send('The person you are checking is a bad person')
        
        shoot = False
        await ctx.send('Morning comes')
        if(death != None or death_w != None):
            if(death != None and death_w != None and death != death_w):
                print(death, death_w)
                await ctx.send('Last night, both' + str(death) + 'and' + str(death_w[1]) + 'died! How terrible!')
                position1 = 0
                position2 = 0
                for key1, value1 in player_name.items():
                    if value1[0].name == death:
                        position1 = key1
                
                for key2, value2 in player_name.items():
                    if value2[0].name == death_w[1]:
                        position2 = key2

                if(player_name[position1] == 'hunter'or player_name[position2] == 'hunter'):
                    shoot = True

                player_name.pop(position1)
                player_role_list.pop(position1)

                player_name.pop(position2)
                player_role_list.pop(position2)

            elif(death != None and (death_w == None or death_w == death)):
                print(death)
                await ctx.send('Last night' + str(death) + 'died! How terrible!')
                position1 = 0
                for key1, value1 in player_name.items():
                    if value1[0].name == death:
                        position1 = key1

                if(player_name[position1] == 'hunter'):
                    shoot = True

                player_name.pop(position1)
                player_role_list.pop(position1)
            elif((death == None or death == death_w) and death_w != None):
                print(death_w)
                await ctx.send('Last night' + str(death_w[1]) + 'died! How terrible!')
                position1 = 0
                for key1, value1 in player_name.items():
                    if value1[0].name == death_w[1]:
                        position1 = key1

                if(player_name[position1] == 'hunter'):
                    shoot = True

                player_name.pop(position1)
                player_role_list.pop(position1)
        else:
            await ctx.send('Nobody died tonight!')
        
        await ctx.send('The town gathers and meets. Each remaining player has 60 seconds to make their case')
        
        if(player_num >= 8):
            player_name, player_role_list = hunter(shoot, player_role_list, player_name, ctx, client)

        shoot = False

        if (check_game_end(player_role_list) == True):
            break
        
        player_key_list = list(player_name.keys())

        for i in range(player_num):
            if(i in player_key_list):
                await ctx.send('It is now' + str(player_name[i][0].name) + "'s turn to speak")
                await ctx.send("You have 60 seconds!")
                await asyncio.sleep(5)

        global general_meeting
        general_meeting = True

        view = GPPoll(ctx, 15, client, player_name_list)
        await ctx.send('Select the person you want to vote out!', view=view)
        await asyncio.sleep(15)

        vote_off = max(selected, key = selected.count)

        await ctx.send(str(vote_off) + ' got voted off!')

        position1 = 0
        for key1, value1 in player_name.items():
            if value1[0] == vote_off:
                position1 = key1

            if(player_name[position1][1] == 'hunter'):
                shoot = True

        player_name.pop(position1)
        player_role_list.pop(position1)

        print(player_role_list)
        if(player_num >= 8):
            player_name, player_role_list = hunter(shoot, player_role_list, player_name, ctx, client)

        round += 1

    num_werewolves = 0
    num_others = 0
    for role in player_role_list:
        if role == 2:
            num_werewolves += 1
        else:
            num_others += 1
    
    if(num_werewolves >= num_others):
        await ctx.send('The werewolves are victorious!')
    else:
        await ctx.send('The good guys are victorious!')

class Util(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='', # brief and description are what show up in the help menu
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
        view = Poll(ctx,int(seconds), self.client)
        await ctx.send('Do you want to join the current game session?', view=view)    
    # add this cog to the client

async def setup(client):
    await client.add_cog(Util(client))
