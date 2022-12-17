from core.bot import FireDog

import discord

from dotenv import load_dotenv

from os import getenv


load_dotenv()
bot = FireDog(
    intents=discord.Intents.all(),
    command_prefix="fd!"
)


bot.run(getenv("TOKEN"))