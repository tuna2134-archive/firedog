from discord.ext import commands
import discord

from aiomysql import create_pool, Pool

from os import getenv


class FireDog(commands.Bot):
    pool: Pool | None = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    async def setup_hook(self) -> None:
        await self.load_extension("jishaku")

        # Connecting to database
        self.pool = await create_pool(
            host=getenv("DB_HOST"),
            port=int(getenv("DB_PORT")),
            user=getenv("DB_USER"),
            password=getenv("DB_PASSWORD"),
            db=getenv("DB_NAME"),
            autocommit=True
        )

        # Loading cogs
        await self.load_extension("cogs.auth")
        await self.load_extension("cogs.bot")

    async def on_ready(self) -> None:
        print(self.user.name)

    async def is_owner(self, user: discord.User) -> bool:
        return user.id in [739702692393517076]