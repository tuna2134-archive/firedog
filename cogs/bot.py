# Cog - bot
from discord.ext import commands, tasks
from discord import app_commands
import discord

from time import time
import sys


class Bot(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.pool = bot.pool
        self.change_presence.start()

    @tasks.loop(minutes=2.0)
    async def change_presence(self) -> None:
        await self.bot.change_presence(
            status=discord.Status.online, activity=discord.Activity(
                name=f"{len(self.bot.guilds)}サーバー｜{len(self.bot.users)}ユーザー",
                type=discord.ActivityType.watching
            )
        )

    @change_presence.before_loop
    async def wait_ready(self) -> None:
        await self.bot.wait_until_ready()

    def cog_unload(self) -> None:
        self.change_presence.cancel()

    @app_commands.command(description="botの速度を返します。")
    async def ping(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title="Pong!", color=discord.Color.blue())
        embed.add_field(
            name="WebSocket",
            value=f"{round(self.bot.latency * 1000, 2)}ms"
        )
        embed.add_field(name="Http", value="測定中...")
        before = time()
        await interaction.response.send_message(embed=embed)
        embed.set_field_at(
            1, name="Http",
            value=f"{round((time() - before) * 1000, 2)}ms"
        )
        await interaction.edit_original_response(embed=embed)

    @app_commands.command(description="このbotについて。")
    async def info(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(
            title="Info",
            description="このボットで荒らし対策ができる！をモットに作っています。",
            color=discord.Color.blue()
        )
        embed.add_field(name="サーバー導入数", value=f"{len(self.bot.guilds)}サーバー")
        embed.add_field(name="認識できるユーザー数", value=f"{len(self.bot.users)}ユーザー")
        py_info = sys.version_info
        embed.add_field(
            name="Python",
            value=f"v{py_info.major}.{py_info.minor}.{py_info.micro}"
        )
        embed.add_field(
            name="discord.py",
            value=f"v{discord.__version__}")
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Bot(bot))
