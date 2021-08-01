from discord.embeds import Embed
from discord.ext.commands import Cog,command
from discord.mentions import AllowedMentions
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option
import datetime
from discord import Colour
from apscheduler.triggers import date


class Announcements(Cog):

    def __init__(self,client):
        self.client = client
        self.channelId = 848526709800304691

    @command(name= 'announce', aliases= ['Announce', 'a'])
    async def announcement(self,ctx):
        pass

    @cog_ext.cog_slash(
        name='announcement',
        guild_ids=[848413322197073952],
        description='Make an announcement on a particular date',
        options=[
                create_option(
                    name="title",
                    description="The title of your announcement",
                    required=True,
                    option_type=3
                ),
                create_option(
                    name="content",
                    description="The content of your announcement",
                    required=True,
                    option_type=3
                ),
                create_option(
                    name="hour",
                    description="The hour to make the announcement on, if not given defaults to now.",
                    required=False,
                    option_type=4
                ),
                create_option(
                    name="date",
                    description="The date to make the announcement on, if not given defaults to now.",
                    required=False,
                    option_type=4
                ),
                create_option(
                    name="month",
                    description="The month to make the announcement on, if not given defaults to now.",
                    required=False,
                    option_type=4
                ),
                create_option(
                    name="year",
                    description="The year to make the announcement on, if not given defaults to now.",
                    required=False,
                    option_type=4
                ),
                create_option(
                    name="role",
                    description="Specific Role to tag, no need to select @everyone, its the default",
                    required=False,
                    option_type=8
                ),
            ]
        )
    async def announcements(self, ctx:SlashContext, title:str, content:str, hour:int = None, day:int = None, month:int = None, year:int = None, role:str = '@everyone '):

        await ctx.defer()

        async def send_announcement():

            if role!='@everyone ':
                embed = Embed(title=title, description = f'{role.mention} \n'+content, color = Colour.from_rgb(198, 197, 255))
                embed.set_footer(
                    text = datetime.datetime.now().strftime("%d %b, %Y"),
                    icon_url=ctx.author.avatar_url if ctx.author.avatar_url is not None else None
                    )
                await ctx.channel_by_id(self.channelId).send(embed=embed, allowed_mentions=AllowedMentions.all())

            else:
                embed = Embed(title=title, description = f'{role} \n'+content, color = Colour.from_rgb(198, 197, 255))
                embed.set_footer(
                    text = datetime.datetime.now().strftime('%d %b, %Y'),
                    icon_url=ctx.author.avatar_url if ctx.author.avatar_url is not None else None
                    )
                await ctx.channel_by_id(self.channelId).send(embed=embed, allowed_mentions=AllowedMentions.all())
        

        def a_scheduler(sched):
            sched.add_job(send_announcement, date.DateTrigger(run_date=date_input))
            print('Scheduled')

        if (day is not None and month is not None and year is not None and hour is not None):

            date_input = datetime.datetime(
                year,
                month,
                day,
                hour,
                (datetime.datetime.now().minute)+1,
                datetime.datetime.now().second
                )
            print(date_input)

            if (date_input>datetime.datetime.now()):
                await ctx.send("Announcement scheduled")
                a_scheduler(self.client.scheduler)

            else:
                await ctx.send("Invalid date given")
                
        else:
            await ctx.send("Announced Now")
            await send_announcement()


def setup(client):
    client.add_cog(Announcements(client))