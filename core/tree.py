# Core - tree
from discord.app_commands import (
    CommandTree,
    AppCommandError,
    CommandOnCooldown
)
import discord
from traceback import TracebackException


class ErrorView(discord.ui.View):

    def __init__(self, error: AppCommandError):
        super().__init__(timeout=180)
        self.error = error

    @discord.ui.button(label="詳細", emoji=":arrow_down:")
    async def describe(
        self, interaction: discord.Interaction, style: discord.ButtonStyle
    ):
        content = TracebackException.from_exception(self.error)
        await interaction.response.send_message(embed=discord.Embed(
            title="例外エラー2",
            description=f"```py\n{str(content)}\n```0",
            color=discord.Color.red()
        ))


class FiredogTree(CommandTree):

    async def on_error(
        self, interaction: discord.Interaction, error: AppCommandError
    ) -> None:
        if isinstance(error, CommandOnCooldown):
            await interaction.response.send_message(embed=discord.Embed(
                title="クールダウンエラー",
                description=f"負荷防止のため、{round(error.retry_after, 2)}"
                "秒後にお試しください。",
                color=discord.Color.red()
            ), ephemeral=True)
        else:
            await interaction.response.send_message(embed=discord.Embed(
                title="例外エラー",
                description=error,
                color=discord.Color.red()
            ))
