# Cog - bot
from discord.ext import commands, tasks
from discord import app_commands, permissions
import discord

from time import time
import sys


class Bot(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.pool = bot.pool
        self.change_presence.start()
        per = discord.Permissions.none()
        per.manage_roles = True
        per.manage_messages = True
        self.invite_url = discord.utils.oauth_url(
            bot.user.id, permissions=per
        )

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
            title="このボットの情報",
            description="このボットで荒らし対策ができる！をモットに作っています。",
            color=discord.Color.blue()
        )
        embed.add_field(name="サーバー導入数", value=f"{len(self.bot.guilds)}サーバー")
        embed.add_field(name="認識できるユーザー数", value=f"{len(self.bot.users)}人")
        py_info = sys.version_info
        embed.add_field(
            name="Python",
            value=f"v{py_info.major}.{py_info.minor}.{py_info.micro}"
        )
        embed.add_field(
            name="discord.py",
            value=f"v{discord.__version__}"
        )
        embed.add_field(
            name="開発者",
            value="[tuna2134](https://github.com/tuna2134)"
        )
        embed.add_field(
            name="GitHub",
            value="[tuna2134/firedog](https://github.com/tuna2134/firedog)"
        )
        await interaction.response.send_message(embed=embed)


    @app_commands.command(description="ボットの招待リンクを表示します。")
    async def invite(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(embed=discord.Embed(
            title="導入検討ありがとうございます！",
            description=f"導入リンクは[こちら]({self.invite_url})です。",
            color=discord.Color.blue()
        ), ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Bot(bot))
