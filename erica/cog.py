from discord import Embed
from discord.ext import commands


class Cog(commands.Cog):

    def __init__(self, name, color=0x0):
        self.name = name
        self.color = color

    def create_embed(self, title, description=None):
        em = Embed(title=title, description=description, color=self.color)
        em.set_author(name=self.name)
        return em
