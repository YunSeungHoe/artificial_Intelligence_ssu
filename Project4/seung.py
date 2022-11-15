import discord
import os
import asyncio
import pandas as pd

df = pd.read_excel("artest.xlsx", engine = "openpyxl")
discord_token ='MTA0MTk4MzQ3NTAyNjIzOTU0OA.GCOUgo.RaCP0H1MIGGBP96GXZCyjkLfHeu_wdAF5tl7yw'
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
    row_len = df.count()[0]
    for i in range(0, row_len):
        or_list = list(map(str, df.values[i][0].split()))
        and_list = list(map(str, df.values[i][1].split()))
        reponse = df.values[i][2]

    if message.author == client.user:
        return
    elif message.content.startswith(or_list[0]):
        await message.channel.send(reponse)

client.run(discord_token)

        