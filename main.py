import disnake
from disnake.ext import commands
from disnake import ApplicationCommandInteraction, Member
from disnake import TextInputStyle

import asyncio

from config import TOKEN

bot = commands.Bot(intents=disnake.Intents.all(), command_prefix="!")


class Ticket(disnake.ui.Modal):
    """Окно обращения в поддержку"""
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

        embed = disnake.Embed(title=f"Обращение в поддержку", color=0xffffff)

        role: disnake.Role = inter.guild.get_role(1369033075392118855)

        for key, value in inter.text_values.items():
            embed.add_field(
                name=key.capitalize(),
                value=value[:1024],
                inline=False,
            )

        embed2 = disnake.Embed(
            title="> 👀 // Уважаемый игрок!",
            description=f"{inter.author.mention}, дождитесь ответа администрации. Для удобности оказания Вам поддержки приложите сообщениями ниже медиа-файлы с Вашей проблемой. Если проблема решена, то нажмите на кнопку ниже.*",
            color=0xffffff
        )

        await channel_help.send(embeds=[embed2, embed], view=Button_Help_ForAdmin())
        await channel_help.send(f"*Пинг Администрации: {role.mention}*")
        await inter.response.send_message("*Обращение успешно создано!*", ephemeral=True)

class Ticket_Join(disnake.ui.Modal):
    """Окно подачи заявки на игру"""
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label="Ник в майнкрафте",
                custom_id="Ник в майнкрафте",
                style=TextInputStyle.short,
            ),
            disnake.ui.TextInput(
                label="Как вы узнали о нас?",
                custom_id="Источник, откуда о нас узнали",
                style=TextInputStyle.paragraph,
            ),
            disnake.ui.TextInput(
                label="Расскажите кратко о себе?",
                custom_id="Рассказ о себе",
                style=TextInputStyle.paragraph
            ),
            disnake.ui.TextInput(
                label="Какие у Вас планы на сервер? Какие цели?",
                custom_id="Цель и планы",
                style=TextInputStyle.paragraph,
                min_length=64
            )
        ]

        super().__init__(
            title="Заявка на игру",
            custom_id="join_play",
            components=components,
        )

    async def callback(self, inter: disnake.ModalInteraction):
        # category = inter.guild.get_channel(1370778367577690243)

        overwrites = {
            inter.guild.default_role: disnake.PermissionOverwrite(read_messages=False),
            inter.author: disnake.PermissionOverwrite(read_messages=True)
        }

        channel_help = await inter.guild.create_text_channel(name=f"Заявка игрок {inter.author}", overwrites=overwrites)

        embed = disnake.Embed(title=f"Заявка на игрока", color=0xffffff)

        role: disnake.Role = inter.guild.get_role(1369033075392118855)

        for key, value in inter.text_values.items():
            embed.add_field(
                name=key.capitalize(),
                value=value[:1024],
                inline=False,
            )
        embed2 = disnake.Embed(
            title="> 👀 // Уважаемый игрок!",
            description=f"*{inter.author.mention}, дождитесь ответа администрации проекта.*",
            color=0xffffff
        )

        await channel_help.send(embeds=[embed, embed2])
        await channel_help.send(f"*Пинг администрации: {role.mention}*")

        await inter.response.send_message("*Заявка успешно создана!*", ephemeral=True)

class Button_Help(disnake.ui.View):
    """Кнопка button_help"""
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label="Обратиться в поддержку", style=disnake.ButtonStyle.red)
    async def confirm(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.send_modal(modal=Ticket())

class Button_Join(disnake.ui.View):
    """Кнопка "Подать заявку" """
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label="Подать заявку на игрока", style=disnake.ButtonStyle.green)
    async def confirm(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.send_modal(modal=Ticket_Join())


class Button_Help_ForAdmin(disnake.ui.View):
    """Кнопка 'Завершить оказание поддержки' """
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label="Завершить оказание поддержки", style=disnake.ButtonStyle.red)
    async def delete(self, button: disnake.ui.Button, inter: disnake.MessageCommandInteraction):
        await inter.channel.delete()

class Button_Join_Admin(disnake.ui.View):
    """Кнопки в окне подачи заявки"""

    def __init__(self):
        super().__init__(timeout=None)
    
    @disnake.ui.button(label="Одобрить заявку ✅", style=disnake.ButtonStyle.green)
    async def agree(self, button: disnake.ui.Button, inter: disnake.MessageCommandInteraction):
        role = inter.guild.get_role(1369033075392118855)

        if role in {inter.user.roles}:
            embed = disnake.Embed(
                title="> ✅ // Ваша заявка одобрена!",
                description=f">>> Уважаемый игрок, дождитесь, когда администрация проекта добавит Вас в вайтлист. Заявку одобрил: {inter.user.mention}",
                color=0xffffff
            )
            await inter.channel.send(embed=embed)
            await inter.channel.send(f"{role.mention}, добавьте игрока в вайтлист!")
        else:
            await inter.response("У вас нет прав на использовании данной кнопки :(")

    @disnake.ui.button(label="Отклонить заявку ❌", style=disnake.ButtonStyle.red)
    async def agree(self, button: disnake.ui.Button, inter: disnake.MessageCommandInteraction):
        role = inter.guild.get_role(1369033075392118855)
        help_channel = inter.guild.get_channel(1446872071685673032)

        if role in {inter.user.roles}:
            embed = disnake.Embed(
                title="> ❌ // Ваша заявка отклонена!",
                description=f">>> Уважаемый игрок, ваша заявка некорректна для игры на нашем сервере. Если у Вас вопросы по оцениваю Вашей заявки, то напишите ниже Вашу жалобу, иначе обратитесь в {help_channel.mention}. Заявку отклонил: {inter.user.mention}",
                color=0xffffff
            )

            await inter.channel.send(embed=embed)
        else:
            await inter.response("У вас нет прав на использовании данной кнопки :(")


@bot.event
async def on_ready():
    print("Bot is ready!")
 

# @bot.event
# async def on_member_join(member: Member):
#     channel: disnake.TextChannel = bot.get_channel(1369025854809833482)
#     channel2: disnake.TextChannel = bot.get_channel(1369025027189510275)

#     embed = disnake.Embed(
#         title="> 🆕 **/ Новый участник присоединился к серверу!**",
#         description=
# f"""
# >>> *{member.mention},*
# *Заходи на наш сервер по IP из {channel2.mention} и получай удовольствие!*
# """,
#         color=0xffffff
#     )

#     await channel.send(embed=embed)


@bot.event
async def on_member_remove(member: Member):
    channel: disnake.TextChannel = bot.get_channel(1444692045221597338)

    embed = disnake.Embed(
        title="> 😔 **/ Участник покинул сервер...**",
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
        title="> 🆘 // Поддержка",
        description=
"""
>>> Если у Вас возникли какие-то проблемы, при игре на нашем сервере, то сделайте обращение в поддержку нашего сервера, нажав на кнопку снизу.
""",
        color=0xffffff
    )

    await inter.channel.send(embed=embed, view=view)


@bot.command()
@commands.has_any_role(1369033075392118855)
async def button_join(inter: ApplicationCommandInteraction):
    view = Button_Join()

    embed = disnake.Embed(
        title="> ✅ // Подача заявки на игру",
        description=
"""
>>> Если Вы хотите начать игру на нашем сервере, то Вам стоит подать заявку с помощью кнопки снизу. Удачной игры ❤️!
""",
    color = 0xffffff
    )

    await inter.channel.send(embed=embed, view=view)


if __name__ == "__main__":
    bot.run(TOKEN)    
