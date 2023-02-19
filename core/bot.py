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
        for cog_name in ["auth", "bot", "mod"]:
            await self.load_extension(f"cogs.{cog_name}")

    async def on_ready(self) -> None:
        print(self.user.name)
        await self.change_presence(
            status=discord.Status.online, activity=discord.Activity(
                name="絶賛稼働中", type=discord.ActivityType.watching
            )
        )

    async def is_owner(self, user: discord.User) -> bool:
        return user.id in [739702692393517076] or await super().is_owner(user)
