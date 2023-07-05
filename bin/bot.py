import discord
import responses
import deets
import secrets_bot

async def send_message(message, user_message, username, channel, server_name):
    try:
        response = responses.get_response(user_message, message, username, channel, server_name)
        await message.channel.send(response)
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
        elif message.channel.name not in deets.DICT_CHANNEL_IDS:
            return
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        server_name = str(message.guild.name)
        await send_message(message, user_message, username, channel, server_name)
    client.run(token=secrets_bot.TOKEN)