class Guard(commands.Cog):
    def init(self, player: discord.member):
        self.player = player
        self.isDead = False
        self.last_saved = ""

    async def whoToSave(self, players: list):
        if (self.last_saved in players):
            players.remove(self.last_saved)

        person_saved = poll(?, 1, "Who do you want to save?", players)
        self.last_saved = person_saved
        return person_saved

