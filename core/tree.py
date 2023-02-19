# Core - tree
from discord.app_commands import (
    CommandTree,
    AppCommandError,
    CommandOnCooldown
)
import discord
from traceback import format_exception


class ErrorView(discord.ui.View):

    def __init__(self, error: AppCommandError):
        super().__init__(timeout=180)
        self.error = error

    @discord.ui.button(label="詳細", emoji="⬇️")
    async def describe(
        self, interaction: discord.Interaction, style: discord.ButtonStyle
    ):
        content = "".join(error for error in format_exception(self.error))
        await interaction.response.edit_message(embed=discord.Embed(
            title="例外エラー2",
            description=f"```py\n{str(content)}\n```",
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
                description=f"```py\n{error}\n```",
                color=discord.Color.red()
            ), view=ErrorView(error))
