import discord
from discord import app_commands
from discord.ui import Select, View
from connection import Connection
import os
# from discord_slash import Slashcommand

TOKEN = os.getenv('DC_TOKEN')
DCID = os.getenv('DC_ID')

intents_setting = discord.Intents.all()
client = discord.Client(intents=intents_setting)
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=DCID))
    print('ready')
    
@tree.command(
    name='find', 
    guild=discord.Object(id=DCID), 
    description='查詢阿北公寓圖片'
)
async def on_message(ctx:discord.Interaction, msg:str):
    slash_user = ctx.user.id
    data_list = Connection().get_all_data(msg)
    if data_list:
        output = make_optional(data_list)
        select = Select(
            placeholder="選擇圖片",
            options=output
        )
        
        async def callback(ctx:discord.Interaction):
            select_user = ctx.user.id
            if slash_user != select_user:
                return ''
            image_id = select.values[0]
            find_pic = discord.File(f'cat/{image_id}.png')
            await ctx.response.send_message(file=find_pic)
        view = View()
        view.add_item(select)
        select.callback = callback
        await ctx.response.send_message(view=view, ephemeral=True, delete_after=10.0)
    else:
        find_pic = discord.File('find.png')
        await ctx.response.send_message(file=find_pic, ephemeral=True)
    


def make_optional(data_list):
    output = []
    for data in data_list:
        output.append(
            discord.SelectOption(
                label=data[1],
                value=int(data[0])-1
            )
        )
    return output
    
    
if __name__ == '__main__':
    client.run(TOKEN)


