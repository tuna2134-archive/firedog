# Cog - bot
from discord.ext import commands
from discord import app_commands
import discord


class Bot(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.pool = bot.pool

    @app_commands.command(description="botの速度を返します。")
    async def ping(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(embed=discord.Embed(
            title="Pong!"
        ).add_field(
            name="WebSocket",
            value=f"{round(self.bot.latency * 1000, 2)}ms"
        ))

    @app_commands.command(description="このbotについて。")
    async def info(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(
            title="Info",
            descrption="このボットで荒らし対策ができる！をモットに作っています。",
            color=discord.Color.blue()
        )
        embed.add_field(name="サーバー導入数", value=f"{len(self.bot.guilds)}サーバー")
        embed.add_field(name="認識できるユーザー数", value=f"{len(self.bot.users)}ユーザー")
        embed.add_field(
            name="WebSocket",
            value=f"{round(self.bot.latency * 1000, 2)}ms"
        )
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Bot(bot))
