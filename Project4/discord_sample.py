import discord
import os
import asyncio

discord_token ='NULL'

# print(discord_token)
print("discord bot starting...")
client = discord.Client(intents=discord.Intents.default())


@client.event
async def on_ready():
    print("Hello We logged in as {}".format(client))
    print('I am {}'.format(client.user.name))
    print('My ID is {}'.format(client.user.id))

@client.event
async def on_message(message : discord.Message):
    print('get message')
    print(message.content)
    if message.author == client.user:
        return
    elif message.content.startswith('hello'):
        print('###')
        await message.channel.send('Hello!')

client.run(discord_token)

        
