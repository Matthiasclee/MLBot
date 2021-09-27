import discord
import shlex
from discord.ext.commands import has_permissions
import requests
import json

client = discord.Client()
badwords = open('badwords.txt','r').read().split("\n")

@client.event
async def on_ready():
	print("Bot ready!")

@client.event
async def on_message(message):
	if message.author == client.user:
		return
	if message.content.startswith("-"): #If message starts with bot prefix
		command = shlex.split(message.content.replace("-", "", 1))[0]
		params = shlex.split(message.content.replace("-", "", 1))

		if command == "help":
			# await message.channel.send("")
			embed=discord.Embed(title="ML Bot", description = "Invite: https://dsc.gg/mlbot", color=0xffffff)
			embed.add_field(name="help", value="Usage: -help\nShows this list", inline=False)
			embed.add_field(name="mute", value="Usage: -mute <user>\nMutes a user (Requires there to be a role named \"Muted\")", inline=False)
			embed.add_field(name="unmute", value="Usage: -unmute <user>\nUnmutes a user", inline=False)
			embed.add_field(name="jail", value="Usage: -jail <user>\nPuts a user in jail (Requires there to be a role named \"Jail\")", inline=False)
			embed.add_field(name="unjail", value="Usage: -unjail <user>\nTakes a user out of jail", inline=False)
			embed.add_field(name="nick", value="Usage: -nick <user> <nickname>\nChanges the nickname of a user", inline=False)
			embed.add_field(name="kick", value="Usage: -kick <user>\nKicks a user", inline=False)
			embed.add_field(name="ban", value="Usage: -ban <user>\nBans a user", inline=False)
			embed.add_field(name="addrole", value="Usage: -addrole <user> <role name>\nGives a user a role", inline=False)
			embed.add_field(name="removerole", value="Usage: -removerole <user> <role name>\nRemoves a role from a user", inline=False)
			await message.channel.send(embed = embed)

		if command == "mute":
			if str(message.author.guild_permissions.manage_messages) == "True":
				user = message.mentions[0]
				guild = message.guild
				role = discord.utils.get(guild.roles, name = "Muted")
				await user.add_roles(role)
				embed=discord.Embed(title="User Muted", description=user.mention + " was muted.", color=0x51ff00)
				await message.channel.send(embed = embed)
			else:
				embed=discord.Embed(title="Insufficient Permisssion", description=message.author.mention + ", you do not have permission to run this command. You need the manage server permission.", color=0xfc0303)
				await message.channel.send(embed = embed)

		if command == "jail":
			if str(message.author.guild_permissions.manage_messages) == "True":
				user = message.mentions[0]
				guild = message.guild
				role = discord.utils.get(guild.roles, name = "Jail")
				await user.add_roles(role)
				embed=discord.Embed(title="User Jailed", description=user.mention + " was jailed.", color=0x51ff00)
				await message.channel.send(embed = embed)
			else:
				embed=discord.Embed(title="Insufficient Permisssion", description=message.author.mention + ", you do not have permission to run this command. You need the manage server permission.", color=0xfc0303)
				await message.channel.send(embed = embed)

		if command == "unmute":
			if str(message.author.guild_permissions.manage_messages) == "True":
				user = message.mentions[0]
				guild = message.guild
				role = discord.utils.get(guild.roles, name = "Muted")
				await user.remove_roles(role)
				embed=discord.Embed(title="User Un-Muted", description=user.mention + " was un-muted.", color=0x51ff00)
				await message.channel.send(embed = embed)
			else:
				embed=discord.Embed(title="Insufficient Permisssion", description=message.author.mention + ", you do not have permission to run this command. You need the manage server permission.", color=0xfc0303)
				await message.channel.send(embed = embed)
		if command == "unjail":
			if str(message.author.guild_permissions.manage_messages) == "True":
				user = message.mentions[0]
				guild = message.guild
				role = discord.utils.get(guild.roles, name = "Jail")
				await user.remove_roles(role)
				embed=discord.Embed(title="User Un-Jailed", description=user.mention + " was un-jailed.", color=0x51ff00)
				await message.channel.send(embed = embed)
			else:
				embed=discord.Embed(title="Insufficient Permisssion", description=message.author.mention + ", you do not have permission to run this command. You need the manage server permission.", color=0xfc0303)
				await message.channel.send(embed = embed)
		if command == "addrole":
			if str(message.author.guild_permissions.manage_messages) == "True":
				user = message.mentions[0]
				guild = message.guild
				role = discord.utils.get(guild.roles, name = params[2])
				await user.add_roles(role)
				embed=discord.Embed(title="Role Added", description=user.mention + " was given the " + params[2] + " role.", color=0x51ff00)
				await message.channel.send(embed = embed)
			else:
				embed=discord.Embed(title="Insufficient Permisssion", description=message.author.mention + ", you do not have permission to run this command. You need the manage server permission.", color=0xfc0303)
				await message.channel.send(embed = embed)
		if command == "removerole":
			if str(message.author.guild_permissions.manage_messages) == "True":
				user = message.mentions[0]
				guild = message.guild
				role = discord.utils.get(guild.roles, name = params[2])
				await user.remove_roles(role)
				embed=discord.Embed(title="Role Removed", description=user.mention + " was removed from the " + params[2] + " role.", color=0x51ff00)
				await message.channel.send(embed = embed)
			else:
				embed=discord.Embed(title="Insufficient Permisssion", description=message.author.mention + ", you do not have permission to run this command. You need the manage server permission.", color=0xfc0303)
				await message.channel.send(embed = embed)
		if command == "kick":
			if str(message.author.guild_permissions.manage_messages) == "True":
				user = message.mentions[0]
				guild = message.guild
				await user.kick()
				embed=discord.Embed(title="User Kicked", description=user.mention + " was kicked.", color=0x51ff00)
				await message.channel.send(embed = embed)
			else:
				embed=discord.Embed(title="Insufficient Permisssion", description=message.author.mention + ", you do not have permission to run this command. You need the manage server permission.", color=0xfc0303)
				await message.channel.send(embed = embed)
		if command == "ban":
			if str(message.author.guild_permissions.manage_messages) == "True":
				user = message.mentions[0]
				guild = message.guild
				await user.ban()
				embed=discord.Embed(title="User Banned", description=user.mention + " was banned.", color=0x51ff00)
				await message.channel.send(embed = embed)
			else:
				embed=discord.Embed(title="Insufficient Permisssion", description=message.author.mention + ", you do not have permission to run this command. You need the manage server permission.", color=0xfc0303)
				await message.channel.send(embed = embed)
		if command == "nick":
			if str(message.author.guild_permissions.manage_messages) == "True":
				user = message.mentions[0]
				guild = message.guild
				await user.edit(nick=params[2])
				embed=discord.Embed(title="Nickname Changed", description=user.mention + "'s nickname was changed.", color=0x51ff00)
				await message.channel.send(embed = embed)
			else:
				embed=discord.Embed(title="Insufficient Permisssion", description=message.author.mention + ", you do not have permission to run this command. You need the manage server permission.", color=0xfc0303)
				await message.channel.send(embed = embed)
	if any(word in message.content.lower() for word in badwords):
		await message.delete()
		embed=discord.Embed(title="Message deleted", description=message.author.mention + ", your message was deleted for containing blocked words.", color=0xfc0303)
		await message.channel.send(embed = embed)




client.run("lol")
