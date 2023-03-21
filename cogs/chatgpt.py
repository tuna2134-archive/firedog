from discord.ext import commands
from discord import app_commands
import discord

from typing import TypedDict

import openai

from os import getenv


openai.api_key = getenv("OPENAI_APIKEY")


def make_embed(message: str):
    return discord.Embed(
        title="ChatGPT",
        description=message
    )


class MessageType(TypedDict):
    role: str
    content: str


class ChatgptView(discord.ui.View):
    def __init__(self, messages: list[MessageType]):
        super().__init__()
        self.messages = messages

    @discord.ui.button(label="返信")
    async def reply(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(ChatgptModal(self.messages))

class ChatgptModal(discord.ui.Modal, title="メッセージの内容"):
    content = discord.ui.TextInput(
        label="コンテンツ",
        placeholder='chatgptに聞きたいことをここに書いてください。'
    )
    def __init__(self, messages: list[MessageType]):
        super().__init__()
        self.messages = messages

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        self.messages.append({
            "role": "user",
            "content": content.value
        })
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=self.messages
        )
        message = response.choices[0]["message"]["content"].strip()
        self.messages.append({
            "role": "assistant",
            "content": message
        })
        await interaction.followup.send(
            embed=make_embed(message),
            view=ChatgptView(self.messages)
        )
            

class Chatgpt(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(description="chatgptと話します")
    @app_commands.describe(content="メッセージ内容")
    async def chatgpt(self, interaction: discord.Interaction, content: str) -> None:
        await interaction.response.defer()
        messages = [
            {
                "role": "user",
                "content": content
            }
        ]
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=messages
        )
        message = response.choices[0]["message"]["content"].strip()
        messages.append({
            "role": "assistant",
            "content": message
        })
        await interaction.followup.send(
            embed=make_embed(message),
            view=ChatgptView(messages)
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Chatgpt(bot))
