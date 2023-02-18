# Core - tree
from discord.app_commands import CommandTree, AppCommandError
import discord


class FiredogTree(CommandTree):

    async def on_error(
        self, interaction: discord.Interaction, error: AppCommandError
    ) -> None:
        await interaction.response.send_message(embed=discord.Embed(
            title="例外エラー",
            description=error,
            color=discord.Color.red()
        ))
