from discord.ext import commands
from discord import app_commands
import discord

from typing import TypedDict

import aiohttp

from os import getenv


def make_embed(message: str):
    return discord.Embed(
        title="Llama",
        description=message
    )


async def talk(promps: str) -> str:
    promps += "\nassistant: "
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://llama-api.tuna2134.jp/", params={"promps": promps}) as res:
            print(await res.read())
            return (await res.json())["content"]


class MessageType(TypedDict):
    role: str
    content: str


def make_promps(messages: list[MessageType]) -> str:
    return "\n".join(f"{msg['role']}: {msg['content']}" for msg in messages)


class LlamaView(discord.ui.View):
    def __init__(self, messages: list[MessageType], author_id):
        super().__init__()
        self.messages = messages
        self.author_id = author_id

    @discord.ui.button(label="返信")
    async def reply(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        if interaction.user.id != self.author.id:
            return await interaction.response.send_message("うーん、君私の主人じゃないでしょ！")
        if len(self.messages) > 5:
            return await interaction.response.send_message("すいません、制限がかかっているためお答えすることができません")
        await interaction.response.send_modal(LlamaModal(self.messages))

class LlamaModal(discord.ui.Modal, title="メッセージの内容"):
    content = discord.ui.TextInput(
        label="コンテンツ",
        placeholder='llamaに聞きたいことをここに書いてください。'
    )
    def __init__(self, messages: list[MessageType]):
        super().__init__()
        self.messages = messages

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        self.messages.append({
            "role": "user",
            "content": self.content.value
        })
        message = await talk(make_promps(self.messages))
        self.messages.append({
            "role": "assistant",
            "content": message
        })
        await interaction.followup.send(
            embed=make_embed(message),
            view=ChatgptView(self.messages)
        )
            

class Llama(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(description="chatgptと話します")
    @app_commands.describe(content="メッセージ内容")
    async def llama(self, interaction: discord.Interaction, content: str) -> None:
        await interaction.response.defer()
        messages = [
            {
                "role": "user",
                "content": content
            }
        ]
        message = await talk(make_promps(messages))
        messages.append({
            "role": "assistant",
            "content": message
        })
        await interaction.followup.send(
            embed=make_embed(message),
            view=LlamaView(messages, interaction.user.id)
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Llama(bot))
