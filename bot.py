# bot.py
import discord
import os
import re
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import datetime
# from datetime import datetime
import pytz
# from pytz import timezone

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.typing = False
intents.presences = False

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
SERVER_ID = 1028780190941335632

print(GUILD)
client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix="!", intents=intents)


async def dm_about_roles(member):
    print(f"DMing {member.name}...")

    await member.send(
        f"""Hi {member.name}, welcome to {member.guild.name}!
         
    Which of these languages do you use:
    * Python
    * JavaScript
    * Go
    * C++    
    
    Reply to this message with one or more of the language names so I can assign you the right roles on our server.
    """
    )


@bot.event
async def on_member_join(member):
    await dm_about_roles(member)


async def assign_roles(message):
    print("Assigning roles...")

    languages = set(re.findall("python|javascript|rust|go|c\+\+",
                    message.content, re.IGNORECASE))

    if languages:
        server = bot.get_guild(SERVER_ID)

        roles = [discord.utils.get(server.roles, name=language.lower())
                 for language in languages]

        member = await server.fetch_member(message.author.id)


@bot.event
async def on_message(message):
    print("Saw a message...")

    if message.author == bot.user:
        return  # prevent responding to self

    if isinstance(message.channel, discord.channel.DMChannel):
        await assign_roles(message)
        return

    if message.content.startswith("!roles"):
        print("HEREERE")
        await dm_about_roles(message.author)
    elif message.content.startswith("!serverid"):
        await message.channel.send(message.channel.guild.id)
    elif message.content.startswith("!setExecMeetingDates"):
        print("sanity check: i feel like im designing test file for cs ;(")
        # await message.channel.send("sanity check: i feel like im designing test file for cs ;(")
        # await set_exec_meeting_dates(message)

@bot.command()
async def set_exec_meeting_dates(ctx, arg): 
    await ctx.send("PPLZ JUST WORK")
    print("sanity check: i feel like im designing test file for cs ;(")
    # print(msg)


@bot.event
async def on_ready():
    await exec_reminder_message()

async def exec_reminder_message():
    while True:
        channel = bot.get_channel(1028780190941335635)
        est_timezone = pytz.timezone("Canada/Eastern") 
        current_time = datetime.datetime.now(est_timezone)
        exec_meeting_time = datetime.datetime(year = current_time.year, 
                                              month = current_time.month, 
                                              day = current_time.day, 
                                              hour = 23, minute = 0,
                                              second = current_time.second,
                                              tzinfo=est_timezone)
        
        time_diff = exec_meeting_time - current_time
        time_diff = round(time_diff.total_seconds() / 60)
        if time_diff == 33:
            await channel.send("@meeting bot tester 15 minutes reminder")
            await asyncio.sleep(60)
        elif time_diff == 20:
            await channel.send("@exec meeting starts rn")
            await asyncio.sleep(60)









bot.run(TOKEN)












# bot asks user in channel instead of dm
# @client.event
# async def on_ready():
#     print(f"""Hi {member.name}, welcome to {member.guild.name}!
#
#     Which of these languages do you use:
#     * Python
#     * JavaScript
#     * Go
#     * C++
#
#     Reply to this message with one or more of the language names so I can assign you the right roles on our server.
#     """)
#
#
# @client.event
# async def on_member_join(member):
#     await member.create_dm()
#     await member.dm_channel.send(
#         f'Hi {member.name}, welcome to my Discord server!'
#     )
#
#
# add events to calendar but need a template to be able to extract date, time, title, etc.
# integrate with Google calendar api
# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
#
#     if 'event' in message.content.lower():
#
#         await message.channel.send('added event to calendar')
#
# client.run(TOKEN)
