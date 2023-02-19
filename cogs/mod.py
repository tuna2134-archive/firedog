# Cog - mod.py
from discord.ext import commands
from discord import app_commands
import discord


class Moderation(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()

    @app_commands.command(description="purge")
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.describe(count="消したいメッセージ数")
    async def purge(self, interaction: discord.Interaction, count: int) -> None:
        await interaction.channel.purge(limit=count)
        await interaction.response.send_message(embed=discord.Embed(
            title="消しました",
            color=discord.Color.blue()
        ), ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Moderation(bot))
