# import base libraries
import json
import os  # to look for commands

# import discord stuff
import discord
from discord.ext import commands


# load the config file
with open('config.json') as f:
    config = json.load(f)

# define bot intents
intents = discord.Intents().default()

# define the bot object itself
bot = commands.Bot(command_prefix=config["prefix"], intents=intents)

# logs to the console once the bot is up and running
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


@bot.command(aliases=["load"])
@commands.is_owner()
async def load_extension(ctx, extension):
    """
    owner-only command used to load cogs
    the cog needs to be unloaded first
    in order to be able to be loaded
    """
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f"Extension {extension} loaded successfully!")


@bot.command(aliases=["unload"])
@commands.is_owner()
async def unload_extension(ctx, extension):
    """
    owner-only command used to unload cogs
    the cog needs to be loaded first
    in order to be able to be unloaded
    """
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send(f"Extension {extension} unloaded successfully!")


@bot.command(aliases=["reload"])
@commands.is_owner()
async def reload_extension(ctx, extension):
    """
    owner-only command used to reload cogs.
    the reloaded cog needs to be loaded in
    order for this command to work
    """
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f"Extension {extension} reloaded successfully!")

[bot.load_extension(f'cogs.{cog[:-3]}') for cog in os.listdir('./cogs/') if cog.endswith('.py')]

# runs the bot
bot.run(config['token'])
