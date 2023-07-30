import discord
import responses
import deets
import secrets_bot
from return_type import return_type
from datetime import datetime
import io


async def send_message(message, user_message, username, channel, server_name):
    try:
        response = responses.get_response(user_message, message, username, channel, server_name)
        if response.type == return_type.TEXT:
            await message.reply(response.ret)
        if response.type == return_type.IMG:
            img_response = discord.File(io.BytesIO(response.data), filename=f'figure - {datetime.now()}.png')
            await message.reply(content=response.ret, file=img_response)
    except Exception as e:
        print(e)

async def send_export(message, user_message, username, channel, server_name):
    try:
        response = responses.get_response(user_message, message, username, channel, server_name).ret
        response = discord.File(response, filename=f'export - {datetime.now()}.csv')
        if (username == secrets_bot.HUNNY_USER):
            await message.reply(content="Export file (csv) attached to this message, my data scientist hunny. :heart:", \
                                       file=response)
        elif (username == secrets_bot.NANA):    
            await message.reply(content="Export file (csv) attached to this message.", \
                                       file=response)
        else:
            await message.channel.send("Export permissions error.")
    except Exception as e:
        print(e)




def run_discord_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print (f'{client.user} has started.')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        elif (str(message.channel.type) == deets.PRIVATE):
            return
        elif message.channel.name not in deets.DICT_CHANNEL_IDS:
            return
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        server_name = str(message.guild.name)

        if (user_message == "!calcexport"):
            await send_export(message, user_message, username, channel, server_name)
        else:
            await send_message(message, user_message, username, channel, server_name)
    client.run(token=secrets_bot.TOKEN)