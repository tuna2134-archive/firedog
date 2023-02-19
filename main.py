from core.bot import FireDog

import discord

from dotenv import load_dotenv
try:
    import uvloop # ignore
except Exception:
    pass
else:
    uvloop.install()

from os import getenv


load_dotenv()
bot = FireDog(
    intents=discord.Intents.all(),
    command_prefix="fd!",
    activity=discord.Activity(
        name="起動中｜Booting...",
        type=discord.ActivityType.watching
    ),
    status=discord.Status.idle
)


bot.run(getenv("TOKEN"))
