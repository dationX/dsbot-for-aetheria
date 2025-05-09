import disnake
from disnake.ext import commands
from disnake import ApplicationCommandInteraction, Member

import asyncio

from config import TOKEN

bot = commands.Bot(intents=disnake.Intents.all(), command_prefix="/")


@bot.event
async def on_ready():
    print("Бот готов!")


@bot.command(name="ping", usage="/ping")
async def ping(inter: ApplicationCommandInteraction):
    await inter.response.send_message("Понг!")


@bot.event
async def on_member_join(member: Member):
    channel: disnake.TextChannel = bot.get_channel(1369025854809833482)
    channel2: disnake.TextChannel = bot.get_channel(1370393239789633556)

    embed = disnake.Embed(
        title="Новый участник присоединился к серверу!",
        description=
f"""
{member.mention},
Подавай заявку на игрока проекта Aetheria в {channel2.mention}
""",
        color=0xffffff
    )

    await channel.send(embed=embed)


@bot.event
async def on_member_remove(member: Member):
    channel: disnake.TextChannel = bot.get_channel(1369025854809833482)

    embed = disnake.Embed(
        title="Участник покинул сервер...",
        description=f"{member.mention}",
        color=0xffffff
    )

    await channel.send(embed=embed)


@bot.command(name="clear", usage="/clear [amount]")
async def clear(inter: ApplicationCommandInteraction, amount):
    await inter.channel.purge(limit=int(amount)+1)
    

bot.run(TOKEN)    
