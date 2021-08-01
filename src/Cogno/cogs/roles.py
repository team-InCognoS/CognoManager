from discord.ext.commands import Cog, command

class RoleGiver(Cog):

    def __init__(self, client):
        self.client = client

def setup(client):
    client.add_cog(RoleGiver(client))