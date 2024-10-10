# Setup stuff in the Config

import nextcord
from nextcord.ext import commands
import json

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

intents = nextcord.Intents.all()

bot = commands.Bot(command_prefix="+", intents=intents)

users = {}

@bot.event
async def on_voice_state_update(member, before, after):
    guild = bot.get_guild(config["guild_id"])

    if after.channel and after.channel.id == config["vc_channel_id"] and member.id not in users:
        category = after.channel.category  
        overwrites = {
            guild.default_role: nextcord.PermissionOverwrite(connect=False),
            member: nextcord.PermissionOverwrite(connect=True, manage_channels=True)
        }

        j2c = await guild.create_voice_channel(f"{member.name}'s channel", category=category, overwrites=overwrites)
        users[member.id] = j2c.id 

        await member.move_to(j2c)

    if before.channel and before.channel.id in users.values() and after.channel != before.channel:
        vc_channel = before.channel
        if len(vc_channel.members) == 0:
            await vc_channel.delete()
            users.pop(member.id, None)

bot.run(config["TOKEN"])
