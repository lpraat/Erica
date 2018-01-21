class MPlayer():

    def __init__(self):
        self.queue = []

class Music():

    def __init__(self, bot):
        self.bot = bot
        self.player = MPlayer()

def setup(bot):
    bot.add_cog(Music(bot))