from __future__ import print_function
import discord
from discord import message
from discord.ext import commands, tasks
from discord.utils import get
from itertools import cycle
import time, asyncio, csv, sys
from PIL import Image, ImageDraw, ImageFont
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '10anpR0gJti9pabLe2yv8CwSY2c7OKzAadylgURpeuu4'
SAMPLE_RANGE_NAME = 'Total!A1'
perms = discord.Intents().all()
cat = commands.Bot(command_prefix="?", intents = perms)
status = cycle(["Status 1", "Status 2"])
stat = discord.Game(name="?help for info")
cat.remove_command("help")


@cat.command()
async def help(ctx):
    embed = discord.Embed(title = "Cat Bot Help", description = "", color = discord.Colour.purple())
    embed.add_field(name = "Timer/Announce", value = "announces the Batch Points after <secs> seconds", inline = True)
    embed.add_field(name = "Format:", value = "announce <secs>", inline = True)
    await ctx.send(embed = embed)


@cat.command()
async def donecheck(ctx):
    await ctx.guild.get_channel(852060492020580372).send(embed = discord.Embed(description = "Done with station?", color = discord.Colour.purple))

@cat.command()
async def move(ctx, rolename, origin, destination):

    channel = discord.utils.find(lambda c: c.name == origin, ctx.guild.voice_channels)
    if channel is not None:
        originID = channel.id
    channel = discord.utils.find(lambda c: c.name == destination, ctx.guild.voice_channels)
    if channel is not None:
        destinationID = channel.id

    for member in ctx.guild.get_channel(originID).members:
        # await ctx.send(member)
        # await ctx.send(member.roles)

        role = discord.utils.find(lambda r: r.name == rolename, ctx.message.guild.roles)
        if role in member.roles:
            await member.move_to(ctx.guild.get_channel(destinationID))
    await ctx.send("Done.")

@cat.command()
async def scour(ctx, rolename, destination):

    # channel = discord.utils.find(lambda c: c.name == origin, ctx.guild.voice_channels)
    # if channel is not None:
    #     originID = channel.id
    channel = discord.utils.find(lambda c: c.name == destination, ctx.guild.voice_channels)
    if channel is not None:
        destinationID = channel.id

    for voice_channel in ctx.guild.voice_channels:
        for member in voice_channel.members:
            role = discord.utils.find(lambda r: r.name == rolename, ctx.message.guild.roles)
            if role in member.roles:
                await member.move_to(ctx.guild.get_channel(destinationID))

    await ctx.send("Done.")

@cat.command()
async def rotate(ctx, role1, role2, role3, role4, role5, role6, role7, role8, role9):
    rooms = [856014266162348092, 851342425342345237, 851342453932032041, 851734913656029195, 851734980764631040, 851734998599335936, 851735015372095539, 851735032645287956, 851735050935992320]
    assignments = [role1,role2,role3,role4,role5,role6,role7,role8,role9]
    channelList = []

    channelList.append(ctx.guild.get_channel(856141106215780372))
    channelList.append(ctx.guild.get_channel(856138738064556053))

    for roomID in rooms:
        channelList.append(ctx.guild.get_channel(roomID))

    for voice_channel in channelList:
        for member in voice_channel.members:
            for rolename in assignments:
                role = discord.utils.find(lambda r: r.name == rolename, ctx.message.guild.roles)
                if role in member.roles:
                    await ctx.send("found " + member.name)
                    await member.move_to(ctx.guild.get_channel(rooms[assignments.index(rolename)]))

    await ctx.send("Done.")

@cat.command()
async def repop(ctx, role1, role2, role3, role4, role5, role6, role7, role8, role9):
    rooms = [856014266162348092, 851342425342345237, 851342453932032041, 851734913656029195, 851734980764631040, 851734998599335936, 851735015372095539, 851735032645287956, 851735050935992320]
    assignments = [role1,role2,role3,role4,role5,role6,role7,role8,role9]
    channelList = []
    for roomID in rooms:
        # channelList.append(ctx.guild.get_channel(roomID))
            
        for member in ctx.guild.get_channel(843888136231977080).members:
            
            for rolename in assignments:

                role = discord.utils.find(lambda r: r.name == rolename, ctx.message.guild.roles)
                if role in member.roles:
                    await member.move_to(ctx.guild.get_channel(rooms[assignments.index(role)]))

    await ctx.send("Done.")
# @cat.command()
# async def list(ctx):
    # for voice_channel in ctx.guild.voice_channels:
    #     await ctx.send(f"in {voice_channel}:")
    #     for member in voice_channel.members:
    #         await ctx.send(f"\t {member}")
    #         destination = discord.VoiceChannel(851342425342345237)
    #         await member.move_to(destination)

@cat.command()
async def withme(ctx):
    ls = []
    for member in ctx.author.voice.channel.members:
        ls.append(member.name)
    await ctx.send(ls)
    # await ctx.send("text to speech test", tts = True)

@cat.event
async def on_ready():
    print("Cat Ready.") 
    await cat.change_presence(status=discord.Status.do_not_disturb, activity=stat)

@cat.command()
async def timer (ctx, *, secs):
    await ctx.send(embed = discord.Embed(title = f"Timer set for {secs} seconds!", color = discord.Colour.purple()))
    secs = int(secs)
    while secs:
        print(secs)
        if secs == 600 or secs == 300 or secs == 120:
            await ctx.send(embed = discord.Embed(title = f"{int(secs/60)} minutes left!", color = discord.Colour.purple()))
        if secs == 60:
            await ctx.send(embed = discord.Embed(title = "1 minute left!", color = discord.Colour.purple()))
        time.sleep(1)
        secs -= 1

@cat.command()
async def readycheck(ctx):
    # await ctx.guild.get_channel(852060492020580372).send(embed = discord.Embed(title = "React with your station's emote if you're done!", color = discord.Colour.purple()))
    emojis = ['Acad', 'Exte', 'Fin', 'Inte', 'Mem', 'Pub', 'Consti', 'Exe', 'App_Heads']
    message = await ctx.guild.get_channel(852060492020580372).send(embed = discord.Embed(title = "React with your station's emote if you're done!", description = ctx.guild.default_role.name, color = discord.Colour.purple()))
    for emoji in emojis:
        fetched = get(cat.emojis, name = emoji)
        await message.add_reaction(fetched)


# @cat.command()
# async def ping(ctx):
#     global emojis
#     if not emojis:
#         emojis = {e.name:str(e) for e in ctx.bot.emojis}
#     msg = "Pong :CustomEmoji: {0.author.mention}".format(ctx.message).replace(':CustomEmoji:',emojis['CustomEmoji'])
#     await ctx.send(msg)

@cat.command()
async def announce(ctx, *, secs):
    await ctx.send(embed = discord.Embed(title = f"Timer set for {secs} seconds!", color = discord.Colour.purple()))
    secs = int(secs)
    while secs:
        # print(secs)
        if secs == 600 or secs == 300 or secs == 120:
            await ctx.guild.get_channel(852060492020580372).send(embed = discord.Embed(title = f"{int(secs/60)} minutes left!", color = discord.Colour.purple()))
        elif secs == 180:
            # await ctx.guild.get_channel(852060492020580372).send(embed = discord.Embed(title = "React with your station's emote if you're done!", color = discord.Colour.purple()))
            emojis = ['Acad', 'Exte', 'Fin', 'Inte', 'Mem', 'Pub', 'Consti', 'Exe', 'App_Heads']
            message = await ctx.guild.get_channel(852060492020580372).send(embed = discord.Embed(title = "React with your station's emote if you're done!", description = ctx.guild.default_role.name, color = discord.Colour.purple()))
            for emoji in emojis:
                fetched = get(cat.emojis, name = emoji)
                await message.add_reaction(fetched)
        elif secs == 60:
            # await ctx.send("HELLO HELLO HELLO. 1 minute left!", tts = True)
            # await ctx.channel.purge(limit=1)
            await ctx.guild.get_channel(852060492020580372).send(embed = discord.Embed(title = "1 minute left!", color = discord.Colour.purple()))
        time.sleep(1)
        secs -= 1
    
    #SHEETS ACCESS BEGIN DO NOT TOUCH
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])
    GenerateImg(values[0][0])
    await ctx.guild.get_channel(852060492020580372).send(embed = discord.Embed(title = "Time's Up!", description = ctx.guild.default_role.name, color = discord.Colour.purple()))

    scoreEmbed = discord.Embed(title = "Current batch score:", color = discord.Colour.purple())
    file = discord.File("pil_text_font.png", filename="image.PNG")
    scoreEmbed.set_image(url = "attachment://image.PNG")
    # await ctx.send(f"HELLO HELLO HELLO. Sobrang ang Current batch score is {values[0][0]}", tts = True)
    # await ctx.channel.purge(limit=1)
    await ctx.guild.get_channel(852058629741084672).purge(limit=1)
    await ctx.guild.get_channel(852058629741084672).send(file = file, embed = scoreEmbed)

def GenerateImg(score):

    img = Image.new('RGB', (500, 500), color = "white")
    fnt = ImageFont.truetype('C:\Windows\Fonts\consola.ttf', 225)
    d = ImageDraw.Draw(img)
    w,h = d.textsize(score, font=fnt)
    d.text(((500-w)/2, (500-h)/2), score, font=fnt, fill="black")
    
    img.save('pil_text_font.png')


cat.run("ODUwNjUzOTk4NTc4MDA4MTA0.YLs3RQ.wjG5sADoo63Ag8-8-Zh2Mvplse0")