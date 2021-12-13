###########-importing required libraries-###########
from os import name
from io import BytesIO
import discord
from discord.enums import Status
from discord.ext import commands
from dotenv import load_dotenv
import random
from PIL import Image, ImageChops, ImageDraw, ImageFont

def circle(pfp,size = (215,215)):
    
    pfp = pfp.resize(size, Image.ANTIALIAS).convert("RGBA")
    
    bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask) 
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(pfp.size, Image.ANTIALIAS)
    mask = ImageChops.darker(mask, pfp.split()[-1])
    pfp.putalpha(mask)
    return pfp

###########-setting the prefix-###########
client = commands.Bot(command_prefix=';')

###########-checks if the bot ready-###########
@client.event
async def on_ready():
    print('Bot is ready.')


                                            ###########-commands-###########





###########-help command-###########
client.remove_command("help")

@client.group(invoke_without_command=True)
async def help(ctx):
    embed = discord.Embed(title = "Help", color = discord.Colour.blue())
    embed.add_field(name = "Moderation*", value = "kick, ban, mute, clera")
    embed.add_field(name = "Fun", value = "pun, coinflip")
    embed.set_footer(text="❗️ *Only staff members can use moderation commands.")
    await ctx.send(embed = embed)            

###########-memberinfo command-###########
@client.command(name="memberinfo")
@commands.has_permissions(kick_members=True)
async def memberinfo(self,ctx,member:discord.Member=None):
    if not member:
        member = ctx.author

    name, nick, Id, status = str(member), member.display_name, str(member.id), str(member.status).upper()

    created_at = member.created_at.strftime("%a %b\n%B %Y")
    joined_at = member.joined_at.strftime("%a %b\n%B %Y")

    base = Image.open("base.png").convert("RGBA")
    background = Image.open("bg.png").convert("RGBA")

    pfp = member.avatar_url_as(size=256)
    data = BytesIO(await pfp.read())
    pfp = Image.open(data).convert("RGBA")

    name = f"{name[:16]}"

###########-pun command-###########
load_dotenv()

@client.command()
async def pun(ctx):
    
    with open('Jokes.txt', 'r', encoding="utf8") as f:
        joke_list = f.readlines()
    msg = random.choice(joke_list) 
    await ctx.send(msg) 

###########-clear command-###########
@client.command(aliases=['c'])
@commands.has_permissions(manage_messages = True)
async def clear(ctx,amount=2):
    await ctx.channel.purge(limit = amount)

###########-kick command-###########
@client.command(aliases=['k'])
@commands.has_permissions(kick_members = True)
async def kick(ctx,member : discord.Member,*, reason = "No reason provided."):
    guild = ctx.guild
    await member.send(f"You have been kicked from {guild.name}. Reason: "+reason)
    await member.kick(reason=reason)

###########-ban command-###########
@client.command(aliases=['b'])
@commands.has_permissions(ban_members = True)
async def ban(ctx,member : discord.Member,*, reason = "No reason provided."):
    guild = ctx.guild
    await member.send(f"You have been banned from {guild.name}. Reason: "+reason)
    await member.ban(reason=reason)

###########-mute command-###########
@client.command()
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member : discord.Member,*,reason = "No reason provided"):
    guild = ctx.guild
    MutedRole = discord.utils.get(guild.roles, name="Muted")
    
    if not MutedRole:
        MutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(MutedRole, speak=False, send_messages=False, )

    await member.add_roles(MutedRole, reason=reason)
    await ctx.send (f"{member.mention} has been muted for {reason}.")
    await member.send (f"You have been muted in {guild.name} for {reason}.")

###########-unmute command-###########
@client.command()
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    MutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.remove_roles(MutedRole)
    await ctx.send(f"{member.mention} has been unmuted.")

###########-coinflip command-###########
@client.command()
async def coinflip(ctx):
    choices = ["Heads", "Tails"]
    rancoin = random.choice(choices)
    await ctx.send(rancoin)

###########-run the bot-###########
client.run('A TE BOTOD TOKENJE')
