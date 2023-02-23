# Cog - mod.py
from discord.ext import commands
from discord import Role, app_commands
import discord

from typing import List


class RoleSettingSelect(discord.ui.Select):

    def __init__(self, roles: List[discord.Role]):
        options = [discord.SelectOption(
            label=role.id, value=role.mention
        ) for role in roles]
        super().__init__(
            placeholder="ロールを選択してください",
            min_values=1, max_values=len(roles)
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        await interaction.edit_original_response(
            embed=discord.Embed(
                title="役職パネル",
                description="\n".join(role.mention for role in roles)
            )
        )


class RoleSettingView(discord.ui.View):
    
    def __init__(self, roles: List[discord.Role]):
        self.add_item(RoleSettingSelect(roles))


class Moderation(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()

    @app_commands.command(description="メッセージをまとめて消します。")
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.cooldown(2, 30)
    @app_commands.describe(count="消したいメッセージ数")
    async def purge(self, interaction: discord.Interaction, count: int) -> None:
        await interaction.response.defer(ephemeral=True)
        await interaction.channel.purge(limit=count)
        await interaction.followup.send(embed=discord.Embed(
            title="Purge",
            description=f"{count}件消しました。",
            color=discord.Color.green()
        ), ephemeral=True)

    @app_commands.command(description="ロールパネル作成します。")
    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.describe(title="タイトル名")
    async def role(self, interaction: discord.Interaction, title: str) -> None:
        await interaction.response.defer()
        await interaction.followup.send(
            embed=discord.Embed(title="ロール選択してください"),
            view=RoleSettingView(interaction.guild.roles)
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Moderation(bot))
