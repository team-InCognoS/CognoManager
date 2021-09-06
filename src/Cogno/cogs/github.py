from discord.ext.commands import Cog
from discord_slash import cog_ext, SlashContext
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_choice, create_option
from discord import Embed, Color, team
from github import Github
import os

class GithubCommands(Cog):



    def __init__(self,client):
        self.client = client
        self.git = Github(os.getenv("GITHUB_TOKEN"))
        self.repos = list(self.git.get_user("team-InCognoS").get_repos())
        

    @cog_ext.cog_slash(
        name= "rep_info",
        description= "Fetches the info of the given repo of team-InCognoS",
        guild_ids=[848413322197073952],
        options= [create_option(
            name = "repo_name",
            description= 'The repo whose info is to be fetched.',
            required= True,
            option_type = 3,
        )]
    )
    async def RepoInfo(self, ctx: SlashContext, repo_name: str):
        repoName = 'team-InCognoS/'+ repo_name
        repoSelected = ''
        for repo in self.repos:
            if repo.full_name == repoName:
                repoSelected = repo

        readme = str(repoSelected.get_readme().decoded_content,encoding='utf-8').replace("</br>", '\n')
        cloneUrl = repoSelected.clone_url
        url = repoSelected.owner.avatar_url
        languages_used = list(repoSelected.get_languages())
        lang_emb = ''
        for lang in languages_used:
            lang_emb+=f'{lang}\n'
        embed = Embed(title = repo_name,description = f'{cloneUrl} \n'+readme+f'\n*Languages Used:*\n >>> {lang_emb} ')
        embed.set_thumbnail(url=url)
        await ctx.defer()
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(GithubCommands(client))