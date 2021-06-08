import os
import discord
import typing
import random
import json
import requests
from dotenv import load_dotenv
from discord.ext import commands
load_dotenv()
DISCORD_TOKEN = os.environ['TOKEN']

intents = discord.Intents.default()
intents.members=True
#Prefix
bot = commands.Bot('ecn!', intents=intents)

#Status
@bot.event
async def on_ready():
    print(f'{bot.user} har aktiverats & är aktiv i discord!')

    await bot.change_presence(activity=discord.Game(name="@ ECNNetwork.se"))

#Meddelande när man kommer in
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(851740517611732994)
    embed=discord.Embed(title=f"**Välkommen {member.name}!** 🥳", description=f"Vad roligt att se dig inne här! Hoppas du trivs!")
    embed.set_thumbnail(url=member.avatar_url) 
    await channel.send(embed=embed)
#Auto Roll
    role = discord.utils.get(member.guild.roles, name='Medlem')
    await member.add_roles(role)

#Svarar vid kommand
@bot.command(
  help="Detta kommand säger hej till dig!"
)
async def hej(ctx):
	await ctx.channel.send("hejsan")

#Svarar vid skrift
@bot.event
async def on_message(message):
  if message.content == "paj":
    await message.channel.send("Paj är väldigt gott!")

  await bot.process_commands(message)

#Svarar med namn + text
@bot.command(
	help="Vem är en tönt?",
)
async def tönt(ctx, *args):
	response = ""

	for arg in args:
		response = response + " " + arg + " " + "är en tönt"

	await ctx.channel.send(response)

#ÖL
@bot.command()
async def flaska(ctx, amount: typing.Optional[int] = 99, *, liquid="öl"):
    await ctx.send('{} flaskor av {} finns kvar!'.format(amount, liquid))  

#Slå folk
@bot.command()
async def slå(ctx, members: commands.Greedy[discord.Member], *, reason='Fanns ingen :c'):
    slapped = ", ".join(x.name for x in members)
    await ctx.send('{} blev nyss slagen/slagna! Anledning: {}'.format(slapped, reason))

##API##

#API #1 (Quotes)
@bot.command()
async def inspiration(ctx):
    quote = get_quote()
    await ctx.channel.send(quote)

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return quote

#API #2 (Online spelare)
@bot.command()
async def spelare(ctx):
    status = get_status()
    await ctx.channel.send(status)

def get_status():
  response = requests.get("https://minecraft-mp.com/api/?object=servers&element=detail&key=DmlOOJGNo3293fv4bFuYUvLSyBZM1FlVnQD")
  json_data = json.loads(response.text)
  status = json_data["players"] + " " + "spelare är för tillfället inne på `ECNNetwork.se`"
  return status

#API #3 (Antalet röster)
@bot.command()
async def röster(ctx):
    votes = get_votes()
    await ctx.channel.send(votes)
    embed = discord.Embed()
    embed.description = "Tryck [här](https://minecraft-mp.com/server/283174/vote/) för att rösta. ❤️"
    await ctx.send(embed=embed)

def get_votes():
  response = requests.get("https://minecraft-mp.com/api/?object=servers&element=detail&key=DmlOOJGNo3293fv4bFuYUvLSyBZM1FlVnQD")
  json_data = json.loads(response.text)
  votes = json_data["votes"] + " " + "spelare har röstat på servern!"
  return votes

#API #4 (Hämtar banner)
@bot.command()
async def banner(ctx):
  banner = get_banner()
  await ctx.channel.send(banner)

def get_banner():
  response = requests.get("https://minecraft-mp.com/api/?object=servers&element=detail&key=DmlOOJGNo3293fv4bFuYUvLSyBZM1FlVnQD")
  json_data = json.loads(response.text)
  banner = json_data["banner_url"]
  return banner

##Slut av API##

#Förslag
@bot.command(
  help="För att skriva ett förslag skriver du: ecn!förslag <förslag>"
)
async def förslag(ctx, *, message): 
    await ctx.message.delete()
    msg = await ctx.send(message)
    await msg.add_reaction('👍')
    await msg.add_reaction('👎')

bot.run(os.environ['TOKEN'])

