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
bot = commands.Bot('ecn!', intents=intents)

#status
@bot.event
async def on_ready():
    print(f'{bot.user} har aktiverats & är aktiv i discord!')

    await bot.change_presence(activity=discord.Game(name="@ ECNNetwork.se"))

#Välkommen
#https://stackoverflow.com/questions/63321098/is-it-possible-to-get-channel-id-by-name-in-discord-py
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(851740517611732994)
    embed=discord.Embed(title=f"**Välkommen {member.name}!** 🥳", description=f"Vad roligt att se dig inne här! Hoppas du trivs!")
    embed.set_thumbnail(url=member.avatar_url) 
    await channel.send(embed=embed)

#HEJ
@bot.command(
  help="Detta kommand säger hej till dig!"
)
async def hej(ctx):
	await ctx.channel.send("hejsan")

#PAJ
@bot.event
async def on_message(message):
  if message.content == "paj":
    await message.channel.send("Paj är väldigt gott!")

  await bot.process_commands(message)

#Vem är en tönt?
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

#slå
@bot.command()
async def slå(ctx, members: commands.Greedy[discord.Member], *, reason='Fanns ingen :c'):
    slapped = ", ".join(x.name for x in members)
    await ctx.send('{} blev nyss slagen/slagna! Anledning: {}'.format(slapped, reason))

#api test
@bot.command()
async def inspiration(ctx):
    quote = get_quote()
    await ctx.channel.send(quote)

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return quote

#api test 2
@bot.command()
async def spelare(ctx):
    status = get_status()
    await ctx.channel.send(status)

def get_status():
  response = requests.get("https://minecraft-mp.com/api/?object=servers&element=detail&key=DmlOOJGNo3293fv4bFuYUvLSyBZM1FlVnQD")
  json_data = json.loads(response.text)
  status = json_data["players"] + " " + "spelare är för tillfället inne på `ECNNetwork.se`"
  return status

#api test 3
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

#api test 4
@bot.command()
async def banner(ctx):
  banner = get_banner()
  await ctx.channel.send(banner)

def get_banner():
  response = requests.get("https://minecraft-mp.com/api/?object=servers&element=detail&key=DmlOOJGNo3293fv4bFuYUvLSyBZM1FlVnQD")
  json_data = json.loads(response.text)
  banner = json_data["banner_url"]
  return banner

#förslag
@bot.command(
  help="Om du har ett förslag du vill lägga fram, kan du använda dig av detta kommand! SKriv ecn!förslag <förslag>"
)
async def förslag(ctx, *, message): 
    await ctx.message.delete()
    msg = await ctx.send(message)
    await msg.add_reaction('👍')
    await msg.add_reaction('👎')

#Egen hjälp meny:
#https://www.youtube.com/watch?v=ivXw9VO89jw&t=174s&ab_channel=CodeWithSwastik

bot.run(os.environ['TOKEN'])

