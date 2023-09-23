import discord
from discord.ext import commands
import asyncio
import random

class Game():
    players = {}
    initial_num_players = 0
    hunter = None

    def __init__(self, players):
        """
        players: dictionary mapping player number to a tuple (user, role number)
        """
        self.players = dict(players)
        self.initial_num_players = len(self.players)
        if self.initial_num_players > 7:
            for key, value in self.players:
                if value[1] == #hunter value:
                    self.hunter = key
    
    def check_game_end(self):
        # num of bad guys >= num of good guys
        # num of bad guys = 0
        num_werewolves = 0
        num_others = 0
        for role in self.players.values():
            if role == 1:
                num_werewolves += 1
            else:
                num_others += 1
        
        return num_werewolves >= num_others or num_werewolves == 0
    
    def announce_eliminated_players(self, eliminated_players):
        """
        eliminated_players = set of killed players
        """
        if len(eliminated_players):
            for player in eliminated_players:
                #bot prints that players died
        else:
            #bot prints "No one died!"
        
        if self.hunter != None:
            #print that the hunter now has an opportunity to eliminate someone

    
    def run_game(self):
        # Night time
        eliminated_players = set()
        guard_choice = None

        if self.initial_num_players > 10:
            guard_choice = guard()
        werewolf_choice = werewolf()
        is_poison, witch_choice = witch()
        seer()

        eliminated_players.add(werewolf_choice)
        if is_poison:
            eliminated_players.add(witch_choice)
        if guard_choice != None and guard_choice in eliminated_players:
            eliminated_players.remove(guard_choice)
        
        # Day break
        if len(eliminated_players) > 0:
            for player in eliminated_players:
                self.players.remove(player)
        
        announce_eliminated_players()

        if check_game_end():
            # end_game()
            # announce winners
            return
        
        if self.hunter != None and self.hunter in eliminated_players:
            hunter_choice = hunter()
            self.players.remove(hunter_choice)
            # announce person killed by hunter
            self.hunter = None
            
        if check_game_end():
            # end_game()
            # announce winners
            return
        
        # discussion time - send poll
        voted_member = poll()
        self.players.remove(voted_member)

        if self.hunter != None and self.hunter == voted_member:
            hunter_choice = hunter()
            self.players.remove(hunter_choice)
            # announce person killed by hunter
            self.hunter = None





        

    
