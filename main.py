import os
import discord

#from boto.s3.connection import S3Connection
from utils import default
from utils.data import Bot, HelpFormat
from discord_slash import SlashCommand, SlashContext

#TOKEN = S3Connection(os.environ['DISCORD_TOKEN'])
TOKEN = os.getenv("DISCORD_TOKEN")
#help_command=HelpFormat(),
config = default.config()
print("Logging in...")

bot = Bot(
    command_prefix=config["prefix"], prefix=config["prefix"],
    owner_ids=config["owners"], command_attrs=dict(hidden=True), help_command=None,
    allowed_mentions=discord.AllowedMentions(roles=False, users=True, everyone=False),
    intents=discord.Intents(  # kwargs found at https://discordpy.readthedocs.io/en/latest/api.html?highlight=intents#discord.Intents
        guilds=True, members=True, messages=True, reactions=True, presences=True
    )
)
for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"cogs.{name}")

try:
    #bot.run(config["token"])
    bot.run(TOKEN)    

except Exception as e:
    print(f"Error when logging in: {e}")
