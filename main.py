import disnake
from disnake.ext import commands
from disnake import ApplicationCommandInteraction

from config import TOKEN

bot = commands.Bot(test_guilds=[1369024871601930330], intents=disnake.Intents.all())

@bot.event
async def on_ready():
    print("Бот готов!")


@bot.slash_command()
async def ping(inter: ApplicationCommandInteraction):
    await inter.response.send_message("Понг!")


@bot.slash_command()
async def server(inter: ApplicationCommandInteraction):
    await inter.response.send_message(
        f"Название сервера: {inter.guild.name}\nВсего участников: {inter.guild.members}"
    )


@bot.slash_command()
async def user(inter: ApplicationCommandInteraction):
    await inter.response.send_message(f"Ваш тег: {inter.author}\nВаш ID: {inter.author.id}")


@bot.event()
async def on_member_join(member):
    # role = await disnake.utils.get(guild_id=member.guild.id, role_id=...)
    pass


bot.run(TOKEN)    
