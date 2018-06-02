from discord import Embed


class Cog:
    """
    Cogs can inherit this class to have their own embed creator.
    The embed is characterized by a name and a color.
    """
    def __init__(self, name, color):
        self.name = name
        self.color = color

    def create_embed(self, title, description=None):
        em = Embed(title=title, description=description, color=self.color)
        em.set_author(name=self.name)
        return em
