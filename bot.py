# import base libraries
import json
import os  # to look for commands
import logging  # for logging 

# import discord stuff
import discord
from discord.ext import commands


# load the config file
with open('config.json') as f:
    config = json.load(f)

# define bot intents
intents = discord.Intents().default()
allowed_mentions = discord.AllowedMentions.none()

logging.basicConfig(
    level=logging.INFO,
    format="[%(name)s %(levelname)s] %(message)s"
)


# define the bot class
class CommunityBot(commands.AutoShardedBot):
    """Community bot"""

    def __init__(self, **kwargs):
        self.logger = logging.getLogger('CommunityBot')
        super().__init__(**kwargs)
        self._load_extensions()

    # logs to the console once the bot is up and running
    async def on_ready(self):
        print(f"Bot ready, logged in as {self.user}")

    def _load_extensions(self):
        for cog in os.listdir('./cogs/'):
            if not cog.endswith('.py'):
                continue
            self.logger.debug(f"Attempting to load cog {cog}")
            try:
                self.load_extension(f'cogs.{cog[:-3]}')
            except Exception:
                self.logger.exception(f"Cannot load cog {cog}.")
            else:
                self.logger.info(f"Loaded cog {cog}")


# initialize the bot object itself
bot = CommunityBot(command_prefix=config["prefix"], intents=intents)

# run the bot
bot.run(config['token'])
