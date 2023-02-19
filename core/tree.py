# Core - tree
from discord.app_commands import (
    CommandTree,
    AppCommandError,
    CommandOnCooldown
)
import discord


class FiredogTree(CommandTree):

    async def on_error(
        self, interaction: discord.Interaction, error: AppCommandError
    ) -> None:
        if isinstance(error, CommandOnCooldown):
            await interaction.response.send_message(embed=discord.Embed(
                title="クールダウンエラー",
                description=f"負荷防止のため、{error.retry_after}秒後にお試しください。",
                color=discord.Color.red()
            ))
        else:
            await interaction.response.send_message(embed=discord.Embed(
                title="例外エラー",
                description=error,
                color=discord.Color.red()
            ))
