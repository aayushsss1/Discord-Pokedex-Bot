import discord
import requests
import json
from pokedex import pokedex
import pandas as pd
import pypokedex
from discord.ext import commands
import numpy as np
import os
bot = commands.Bot(command_prefix='{')
pokedex = pokedex.Pokedex()

client = discord.Client()
@client.event
async def on_ready(): #event called when the bot is ready
  print('The bot is logged in as {0.user}'.format(client))
@client.event
async def on_message(message):
  if message.author == client.user: 
    return 
  if message.content == '!pokemon help':
      await message.channel.send('Hello you can check the availability by using the command !poke pokemon_name')  
  elif message.content.startswith('!poke'):
    m=message.content.split(' ')
    name=m[1]  
    await displayembed(name,message)

@bot.command()
async def displayembed(name,message):
    poke = pypokedex.get(name =name)
    pokemon = pokedex.get_pokemon_by_name(name)
    dataframe = pd.json_normalize(pokemon[0])
    df = dataframe[['number','name','species','types','family.evolutionLine']]
    base = [f'hp= {poke.base_stats.hp} ',f'attack= {poke.base_stats.attack} ',f'defense= {poke.base_stats.defense} ',f'sp_atk= {poke.base_stats.sp_atk} ',f'sp_def= {poke.base_stats.sp_def} ',f'speed= {poke.base_stats.speed} ']
    types = ','.join(poke.types)
    evolution = ','.join(df['family.evolutionLine'].values[0])
    species = ','.join(df['species'].values)
    Base = ','.join(base)
    embed = discord.Embed(
        title = 'Pokemon',
        description = name,
        colour = discord.Colour.blue()
    )
    embed.set_footer(text='Have a nice day!')
    embed.set_image(url=f'https://pokeres.bastionbot.org/images/pokemon/{poke.dex}.png')
    embed.set_author(name = 'PokéBot', icon_url='https://static.wikia.nocookie.net/pokemon-fano/images/6/6f/Poke_Ball.png/revision/latest?cb=20140520015336')
    embed.add_field(name = 'Pokemon Number',value = poke.dex,inline=False)
    embed.add_field(name = 'Species',value = species,inline=True)
    embed.add_field(name = 'Type',value = types,inline=True)
    embed.add_field(name = 'Base Stats', value = Base, inline = False)
    embed.add_field(name = 'Evolution Line', value = evolution, inline = False)
    await message.channel.send(embed=embed)

client.run(TOKEN)