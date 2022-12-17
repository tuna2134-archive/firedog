# Lib - GuildLogger
import discord
from discord.ext import commands, tasks


class GuildLogger:
    guild: discord.Guild
    log_channel: discord.TextChannel | None = None
    logs: list[discord.Embed] = []

    def __init__(self, guild: discord.Guild, bot: commands.Bot):
        self.guild = guild
        self.pool = bot.pool

    async def get_log_channel(self) -> int:
        # Get the log channel from the database
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(
                    "SELECT * FROM LogChannel WHERE GuildId = %s;", (self.guild.id,))
                if (data := await cursor.fetchone()):
                    return data[1]
    
    @tasks.loop(minutes=5)
    async def send(self) -> None:
        # Send the logs
        if not self.logs:
            return
        if (channel_id := await self.get_log_channel()):
            self.log_channel = self.guild.get_channel(channel_id)
            for embed_index in range(0, len(self.logs), 10):
                await self.log_channel.send(
                    embeds=self.logs[embed_index:embed_index + 10]
                )
            self.logs = []

    def error(self, title: str, description: str) -> None:
        # Create an error
        self.logs.append(
            discord.Embed(
                title=f"エラー({title})",
                description=description,
                color=discord.Color.red()
            )
        )