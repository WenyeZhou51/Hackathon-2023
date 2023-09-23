class Seer(commans.Cog):
    def init(self, player: discord.member):
        self.player = player
        self.isDead = False
        self.alreadySeen = []

    async def whoToSee(self, players: list):
        for person in self.alreadySeen:
            if (person in players):
                players.remove(person)

        person_seen = poll(?, 1, "Whose role do you want to see?", players)
        self.alreadySeen.append(person_seen)
        # DM the role of the player selected
        return person_seen