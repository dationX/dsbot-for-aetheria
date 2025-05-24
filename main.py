import disnake
from disnake.ext import commands
from disnake import ApplicationCommandInteraction, Member
from disnake import TextInputStyle

import asyncio

from config import TOKEN

bot = commands.Bot(intents=disnake.Intents.all(), command_prefix="!")


class Ticket(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label="Дайте заголовок вашему обращению",
                custom_id="Заголовок",
                style=TextInputStyle.short,
            ),
            disnake.ui.TextInput(
                label="Опишите свою проблему",
                custom_id="Проблема",
                style=TextInputStyle.paragraph,
            ),
        ]

        super().__init__(
            title="Обращение в поддержку",
            custom_id="help",
            components=components,
        )

    async def callback(self, inter: disnake.ModalInteraction):
        category = inter.guild.get_channel(1370778367577690243)

        overwrites = {
            inter.guild.default_role: disnake.PermissionOverwrite(read_messages=False),
            inter.author: disnake.PermissionOverwrite(read_messages=True)
        }

        channel_help = await inter.guild.create_text_channel(name=f"Поддержка {inter.author}", category=category, overwrites=overwrites)

        embed = disnake.Embed(title=f"Обращение в поддержку")

        role: disnake.Role = inter.guild.get_role(1369033075392118855)

        for key, value in inter.text_values.items():
            embed.add_field(
                name=key.capitalize(),
                value=value[:1024],
                inline=False,
            )

        await channel_help.send(
f"""
Уважаемый игрок: {inter.author.mention}, дождитесь ответа администрации проекта,
также для удобности оказания вам поддержки приложите сообщениями ниже медиа-контент
с вашей проблемой. Если проблема решена или потеряла актуальность, то нажмите на кнопку ниже.

Пинг Администрации проекта: {role.mention}
""", embed=embed, view=Button_Help_ForAdmin())

        await inter.response.send_message("Обращение успешно создано!", ephemeral=True)


class Button_Help(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label="Обратиться в поддержку", style=disnake.ButtonStyle.grey)
    async def confirm(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.send_modal(modal=Ticket())


class Button_Help_ForAdmin(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label="Завершить оказание поддержки", style=disnake.ButtonStyle.red)
    async def delete(self, button: disnake.ui.Button, inter: disnake.MessageCommandInteraction):
        await inter.channel.delete()


@bot.event
async def on_ready():
    print("Бот готов!")
 

@bot.event
async def on_member_join(member: Member):
    channel: disnake.TextChannel = bot.get_channel(1369025854809833482)
    channel2: disnake.TextChannel = bot.get_channel(1369025027189510275)

    embed = disnake.Embed(
        title="> 🆕 **/ Новый участник присоединился к серверу!**",
        description=
f"""
>>> *{member.mention},*
*Заходи на наш сервер по IP из {channel2.mention} и получай удовольствие!*
""",
        color=0xffffff
    )

    await channel.send(embed=embed)


@bot.event
async def on_member_remove(member: Member):
    channel: disnake.TextChannel = bot.get_channel(1369025854809833482)

    embed = disnake.Embed(
        title="> 🗨️ **/ Участник покинул сервер...**",
        description=f"> *{member.mention}, ждем твоего возвращения!*",
        color=0xffffff
    )

    await channel.send(embed=embed)


@bot.slash_command(name="clear", description="Чистит сообщения, /clear n")
@commands.has_any_role(1369033075392118855)
async def clear(inter: ApplicationCommandInteraction, amount):
    await inter.channel.purge(limit=int(amount)+1)
    await inter.response.send_message("Сообщения успешно удалены", ephemeral=True)


@bot.command()
@commands.has_any_role(1369033075392118855)
async def button(inter: ApplicationCommandInteraction):
    view = Button_Help()

    embed = disnake.Embed(
        title="> Поддержка",
        description=
"""
>>> Если у вас возникли какие-то проблемы, при игре на нашем сервере, то сделайте обращение в поддержку нашего сервера, нажав на кнопку снизу.
""",
        color=0xffffff
    )

    await inter.channel.send(embed=embed, view=view)
    

if __name__ == "__main__":
    bot.run(TOKEN)    
