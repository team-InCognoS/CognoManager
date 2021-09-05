import discord,os
from discord.ext.commands import Bot as cm
from discord.ext.commands.bot import when_mentioned_or
from discord import AllowedMentions
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
from discord_slash import SlashCommand
from glob import glob
from asyncio import sleep
from discord import Embed, Color

load_dotenv()

PREFIX = ";"
OWNER_ID=[462313177359843328]
COGS=[path.split("\\")[-1][:-3] for path in glob("./src/cogno/cogs/*.py")]


class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self,cog,False)

    def ready_up(self,cog):
        setattr(self,cog,True)
        print(f"{cog} ready!")

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])

class CognoS(cm):

    def __init__(self,**options):
        self.prefix=PREFIX
        self.owner=OWNER_ID
        self.ready=False
        self.cogs_ready= Ready()
        self.scheduler = AsyncIOScheduler()
        super().__init__(
            command_prefix=when_mentioned_or(self.prefix),
            owner_ids= self.owner,
            intents = discord.Intents.all(),
            allowed_mentions = AllowedMentions.all(),
            **options
             )
        self.slash = SlashCommand(self, sync_commands=True)

    async def on_connect(self):
        print("Bot Connected")
    
    async def on_ready(self):
        if not self.ready:
            self.ready=True
            self.scheduler.start()
            print("Bot Ready")

        else:
            print("Bot Reconnected")

        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"this server 🕵🏻‍♀️ "))
        while not self.cogs_ready.all_ready():
            await sleep(0.5)

    async def on_message(self,msg):
        await self.process_commands(msg)

    async def on_member_join(self,member):

        Embed = discord.Embed(title="Welcome", color=Color.from_rgb(198, 197, 255))
        Embed.add_field(name="Hola, Hallo, Bonjour!",
                        value=f"Hi {member.mention}! Welcome to **{member.guild}**! Please follow the rules in #rules channel for the betterment of")
        Embed.set_thumbnail(url=member.guild.icon_url)
        channel = member.guild.system_channel
        await channel.send(embed=Embed)
        
        embed = discord.Embed(title="Welcome", color=Color.from_rgb(198, 197, 255),
                              description=f"Hi {member.mention}! Welcome to **{member.guild}**!")
        embed.set_thumbnail(url=member.guild.icon_url)
        await member.send(embed=embed)
        
    def setup(self):
        for cog in COGS:
            self.load_extension(f"cogno.cogs.{cog}")
            print(f"{cog} cog loaded!")
        print("Setup Complete!")

    def run(self):
        self.setup()
        self.token = os.getenv("DC_TOKEN")
        super().run(self.token, reconnect=True)

InCognoS=CognoS()
