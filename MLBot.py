import discord
import shlex
from discord.ext.commands import has_permissions
import requests
import json
from os.path import exists

client = discord.Client()
# badwords = open('badwords.txt','r').read().split("\n")

@client.event
async def on_ready():
	print("Bot ready!")
	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=str(len(client.guilds)) + " servers"))

	for guild in client.guilds:
		print(guild.name + ": " + str(guild.id))



@client.event
async def on_message(message):
	if exists("bwl/" + str(message.guild.id)):
		badwords = open("bwl/" + str(message.guild.id)).read().split("\n")
	else:
		# badwords = open('badwords.txt','r').read().split("\n")
		fl = open("bwl/" + str(message.guild.id), "w")
		fl.write("bad_words_list_" + str(message.guild.id))
		fl.close()
		badwords = open("bwl/" + str(message.guild.id)).read().split("\n")
	# print(badwords)-
	if any(word in message.content.lower() for word in badwords):
		command = shlex.split(message.content.replace("-", "", 1))[0]
		if command != "bwl":
			await message.delete()
			embed=discord.Embed(title="Message deleted", description=message.author.mention + ", your message was deleted for containing blocked words.", color=0xfc0303)
			await message.channel.send(embed = embed)

	if message.author == client.user:
		return
	if message.content.startswith("-"): #If message starts with bot prefix
		command = shlex.split(message.content.replace("-", "", 1))[0]
		params = shlex.split(message.content.replace("-", "", 1))
		if any(word in message.content.lower() for word in badwords):
			if command != "bwl":
				command = ""
		if command == "help":

			# await message.channel.send("")
			embed=discord.Embed(title="ML Bot", description = "Invite: https://dsc.gg/mlbot", color=0xffffff)
			embed.add_field(name="help", value="Usage: -help\nShows this list", inline=False)
			embed.add_field(name="mute", value="Usage: -mute <user>\nMutes a user (Requires there to be a role named \"Muted\")", inline=False)
			embed.add_field(name="unmute", value="Usage: -unmute <user>\nUnmutes a user", inline=False)
			embed.add_field(name="jail", value="Usage: -jail <user>\nPuts a user in jail (Requires there to be a role named \"Jail\")", inline=False)
			embed.add_field(name="unjail", value="Usage: -unjail <user>\nTakes a user out of jail", inline=False)
			embed.add_field(name="delete", value="Usage: -delete <message id>\nDeletes a message", inline=False)
			embed.add_field(name="nick", value="Usage: -nick <user> <nickname>\nChanges the nickname of a user", inline=False)
			embed.add_field(name="kick", value="Usage: -kick <user>\nKicks a user", inline=False)
			embed.add_field(name="ban", value="Usage: -ban <user> <reason>\nBans a user", inline=False)
			embed.add_field(name="unban", value="Usage: -unban <user id>\nUnbans a user", inline=False)
			embed.add_field(name="addrole", value="Usage: -addrole <user> <role>\nGives a user a role", inline=False)
			embed.add_field(name="removerole", value="Usage: -removerole <user> <role>\nRemoves a role from a user", inline=False)
			embed.add_field(name="rr", value="Usage: -rr <description> <emoji> <role>\nMakes a reacction roles message", inline=False)
			embed.add_field(name="poll", value="Usage: -poll <question> <emoji> <description>\nPosts a poll for users to vote", inline=False)
			embed.add_field(name="results", value="Usage: -results <message id>\nShows the results of a poll", inline=False)
			embed.add_field(name="livepoll", value="Usage: -livepoll <question> <emoji> <description>\nPosts a responsive poll for users to vote", inline=False)
			embed.add_field(name="say", value="Usage: -say <message>\nSays something", inline=False)
			embed.add_field(name="bwl", value="Usage: -bwl <add | remove> <word>\nManages the bad words list", inline=False)
			embed.add_field(name="purge", value="Usage: -purge <messages>\nBulk deletes messages", inline=False)
			await message.channel.send(embed = embed)

		if command == "mute":
			if str(message.author.guild_permissions.manage_roles) == "True" or message.author.id == 815035282054184982:
				user = message.mentions[0]
				guild = message.guild
				role = discord.utils.get(guild.roles, name = "Muted")
				await user.add_roles(role)
				embed=discord.Embed(title="User Muted", description=user.mention + " was muted.", color=0x51ff00)
				await message.channel.send(embed = embed)
			else:
				embed=discord.Embed(title="Insufficient Permissions", description=message.author.mention + ", you do not have permission to run this command. You need the manage roles permission.", color=0xfc0303)
				await message.channel.send(embed = embed)

		if command == "jail":
			if str(message.author.guild_permissions.manage_roles) == "True" or message.author.id == 815035282054184982:
				user = message.mentions[0]
				guild = message.guild
				role = discord.utils.get(guild.roles, name = "Jail")
				await user.add_roles(role)
				embed=discord.Embed(title="User Jailed", description=user.mention + " was jailed.", color=0x51ff00)
				await message.channel.send(embed = embed)
			else:
				embed=discord.Embed(title="Insufficient Permissions", description=message.author.mention + ", you do not have permission to run this command. You need the manage roles permission.", color=0xfc0303)
				await message.channel.send(embed = embed)

		if command == "unmute":
			if str(message.author.guild_permissions.manage_roles) == "True" or message.author.id == 815035282054184982:
				user = message.mentions[0]
				guild = message.guild
				role = discord.utils.get(guild.roles, name = "Muted")
				await user.remove_roles(role)
				embed=discord.Embed(title="User Un-Muted", description=user.mention + " was un-muted.", color=0x51ff00)
				await message.channel.send(embed = embed)
			else:
				embed=discord.Embed(title="Insufficient Permissions", description=message.author.mention + ", you do not have permission to run this command. You need the manage roles permission.", color=0xfc0303)
				await message.channel.send(embed = embed)
		if command == "unjail":
			if str(message.author.guild_permissions.manage_roles) == "True" or message.author.id == 815035282054184982:
				user = message.mentions[0]
				guild = message.guild
				role = discord.utils.get(guild.roles, name = "Jail")
				await user.remove_roles(role)
				embed=discord.Embed(title="User Un-Jailed", description=user.mention + " was un-jailed.", color=0x51ff00)
				await message.channel.send(embed = embed)
			else:
				embed=discord.Embed(title="Insufficient Permissions", description=message.author.mention + ", you do not have permission to run this command. You need the manage roles permission.", color=0xfc0303)
				await message.channel.send(embed = embed)
		if command == "addrole":
			if str(message.author.guild_permissions.manage_roles) == "True" or message.author.id == 815035282054184982:
				user = message.mentions[0]
				guild = message.guild
				role = message.guild.get_role(int(params[2].replace("<", "").replace(">", "").replace("@", "").replace("&", "")))
				await user.add_roles(role)
				embed=discord.Embed(title="Role Added", description=user.mention + " was given the <@&" + str(role.id) + "> role.", color=0x51ff00)
				await message.channel.send(embed = embed)
			else:
				embed=discord.Embed(title="Insufficient Permissions", description=message.author.mention + ", you do not have permission to run this command. You need the manage roles permission.", color=0xfc0303)
				await message.channel.send(embed = embed)
		if command == "removerole":
			if str(message.author.guild_permissions.manage_roles) == "True" or message.author.id == 815035282054184982:
				user = message.mentions[0]
				guild = message.guild
				role = message.guild.get_role(int(params[2].replace("<", "").replace(">", "").replace("@", "").replace("&", "")))
				await user.remove_roles(role)
				embed=discord.Embed(title="Role Removed", description=user.mention + " was removed from the " + params[2] + " role.", color=0x51ff00)
				await message.channel.send(embed = embed)
			else:
				embed=discord.Embed(title="Insufficient Permissions", description=message.author.mention + ", you do not have permission to run this command. You need the manage roles permission.", color=0xfc0303)
				await message.channel.send(embed = embed)
		if command == "kick":
			if str(message.author.guild_permissions.kick_members) == "True" or message.author.id == 815035282054184982:
				user = message.mentions[0]
				guild = message.guild
				await user.kick()
				embed=discord.Embed(title="User Kicked", description=user.mention + " was kicked.", color=0x51ff00)
				await message.channel.send(embed = embed)
			else:
				embed=discord.Embed(title="Insufficient Permissions", description=message.author.mention + ", you do not have permission to run this command. You need the kick members permission.", color=0xfc0303)
				await message.channel.send(embed = embed)
		if command == "ban":
			if str(message.author.guild_permissions.ban_members) == "True" or message.author.id == 815035282054184982:
				user = message.mentions[0]
				guild = message.guild
				if len(params) == 3:
					await user.ban(reason = params[2])
				else:
					await user.ban()
				embed=discord.Embed(title="User Banned", description=user.mention + " was banned.", color=0x51ff00)
				await message.channel.send(embed = embed)
			else:
				embed=discord.Embed(title="Insufficient Permissions", description=message.author.mention + ", you do not have permission to run this command. You need the ban members permission.", color=0xfc0303)
				await message.channel.send(embed = embed)
		if command == "unban":
			if str(message.author.guild_permissions.ban_members) == "True" or message.author.id == 815035282054184982:
				user = await client.fetch_user(int(params[1]))
				await message.guild.unban(user)
				embed=discord.Embed(title="User Unbanned", description=user.mention + " was unbanned.", color=0x51ff00)
				await message.channel.send(embed = embed)
			else:
				embed=discord.Embed(title="Insufficient Permissions", description=message.author.mention + ", you do not have permission to run this command. You need the ban members permission.", color=0xfc0303)
				await message.channel.send(embed = embed)
		if command == "nick":
			if str(message.author.guild_permissions.manage_nicknames) == "True" or message.author.id == 815035282054184982:
				user = message.mentions[0]
				guild = message.guild
				await user.edit(nick=params[2])
				embed=discord.Embed(title="Nickname Changed", description=user.mention + "'s nickname was changed.", color=0x51ff00)
				await message.channel.send(embed = embed)
			elif message.mentions[0] == message.author and message.author.guild_permissions.change_nickname:
				user = message.mentions[0]
				guild = message.guild
				await user.edit(nick=params[2])
				embed=discord.Embed(title="Nickname Changed", description=user.mention + "'s nickname was changed.", color=0x51ff00)
				await message.channel.send(embed = embed)
			else:
				embed=discord.Embed(title="Insufficient Permissions", description=message.author.mention + ", you do not have permission to run this command. You need the manage nicknames permission or the change nickname permission if you are just changing your own nickname.", color=0xfc0303)
				await message.channel.send(embed = embed)
		if command == "rr":
			if str(message.author.guild_permissions.manage_roles) == "True" or message.author.id == 815035282054184982:
				guild = message.guild
				await message.delete()
				embed=discord.Embed(title="Reaction Roles", description=params[1], color=0xffffff)
				rolecount = (len(params) - 2)/2
				x = 0
				while x < rolecount:
					role = message.guild.get_role(int(params[x*2+3].replace("<", "").replace(">", "").replace("@", "").replace("&", "")))
					embed.add_field(name=params[x*2+2], value = format(role.mention), inline=False)
					x = x + 1
				msg = await message.channel.send(embed = embed)
				outdata = str(msg.id) + ",," + str(rolecount) + ",,"
				x = 0
				while x < rolecount:
					await msg.add_reaction(params[x*2+2])
					role = message.guild.get_role(int(params[x*2+3].replace("<", "").replace(">", "").replace("@", "").replace("&", "")))
					outdata = outdata + params[x*2+2] + ".." + str(role.id) + ",,"
					x = x + 1

				print (outdata)
				f = open("rr/" + str(msg.id), "a")
				f.write(outdata + "\n")
				f.close()
			else:
				embed=discord.Embed(title="Insufficient Permissions", description=message.author.mention + ", you do not have permission to run this command. You need the manage roles permission.", color=0xfc0303)
				await message.channel.send(embed = embed)
		if command == "poll":
			await message.delete()
			embed=discord.Embed(title="Poll", description=params[1], color=0xffffff)
			qcount = (len(params) - 2)/2
			x = 0
			while x < qcount:
				embed.add_field(name=params[x*2+2] + ": " + params[x*2+3], value = "** **", inline=False)
				x = x + 1
			msg = await message.channel.send(embed = embed)
			x = 0
			while x < qcount:
				await msg.add_reaction(params[x*2+2])
				x = x + 1
			embed.set_footer(text = "ID: " + str(msg.id))
			await msg.edit(embed = embed)
		if command == "results":
			msgid = params[1]
			msg = await message.channel.fetch_message(msgid)
			poll = msg.embeds[0]
			res = poll.fields
			qcount = len(res)
			trc = 0
			x = 0
			while x < qcount:
				trc = trc + msg.reactions[x].count - 1
				x = x + 1
			x = 0
			embed=discord.Embed(title="Poll Results", description=poll.description, color=0xffffff)
			while x < qcount:
				prc = int(round((msg.reactions[x].count-1)/trc*100))
				aa = round(prc/10)
				bb = 10 - round(prc/10)
				e = 0
				a = ""
				b = ""
				while e < aa:
					a = a + "▓"
					e = e + 1
				e = 0
				while e < bb:
					b = b + "░"
					e = e + 1
				embed.add_field(name=res[x].name.split(": ")[1], value = a + b + " - " + str(prc) + "%", inline=False)
				x = x + 1
			await msg.channel.send(embed = embed)

		if command == "livepoll":
			await message.delete()
			embed=discord.Embed(title="Live Poll", description=params[1], color=0xffffff)
			qcount = (len(params) - 2)/2
			x = 0
			while x < qcount:
				embed.add_field(name=params[x*2+2] + ": " + params[x*2+3], value = "░░░░░░░░░░ - 0%", inline=False)
				x = x + 1
			msg = await message.channel.send(embed = embed)
			x = 0
			while x < qcount:
				await msg.add_reaction(params[x*2+2])
				x = x + 1
			embed.set_footer(text = "ID: " + str(msg.id))
			await msg.edit(embed = embed)
			f = open("livepoll/" + str(msg.id), "a")
			f.write("" + "\n")
			f.close()
			
		if command == "delete":
			if str(message.author.guild_permissions.manage_messages) == "True" or message.author.id == 815035282054184982:
				msgid = params[1]
				msg = await message.channel.fetch_message(msgid)
				await msg.delete()
			else:
				embed=discord.Embed(title="Insufficient Permissions", description=message.author.mention + ", you do not have permission to run this command. You need the manage messages permission.", color=0xfc0303)
				await message.channel.send(embed = embed)

		if command == "say":
			await message.channel.send(params[1])
			await message.delete()

		if command == "bwl":
			if str(message.author.guild_permissions.administrator) == "True" or message.author.id == 815035282054184982:
				if len(params) == 1:
					embed = discord.Embed(title="Blocked Words List", description = "** **", color=0xffffff)
					x = 0
					while x < len(badwords):
						if x > 0:
							embed.add_field(name=badwords[x], value="** **", inline=False)
						x = x + 1
					await message.channel.send(embed = embed)

				if len(params) == 3:
					if params[1] == "add":
						f = open("bwl/" + str(message.guild.id), "a")
						f.write("\n" + params[2].lower())
						f.close()
						embed=discord.Embed(title="Word blocked", description=params[2] + " was successfully blocked", color=0x51ff00)
						await message.channel.send(embed = embed)
					if params[1] == "remove":
						bw = open("bwl/" + str(message.guild.id), "r").read()
						f = open("bwl/" + str(message.guild.id), "w")
						a = bw.replace("\n" + params[2], "", 1)
						f.write(a)
						f.close()
						embed=discord.Embed(title="Word unblocked", description=params[2] + " was successfully unblocked", color=0x51ff00)
						await message.channel.send(embed = embed)
			else:
				embed=discord.Embed(title="Insufficient Permissions", description=message.author.mention + ", you do not have permission to run this command. You need the administrator permission.", color=0xfc0303)
				await message.channel.send(embed = embed)
		if command == "purge":
			if str(message.author.guild_permissions.manage_messages) == "True" or message.author.id == 815035282054184982:
				await message.channel.purge(limit = int(params[1]) + 1)
			else:
				embed=discord.Embed(title="Insufficient Permissions", description=message.author.mention + ", you do not have permission to run this command. You need the manage messages permission.", color=0xfc0303)
				await message.channel.send(embed = embed)				

@client.event
async def on_guild_join(guild):
	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=str(len(client.guilds)) + " servers"))

@client.event
async def on_guild_remove(guild):
	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=str(len(client.guilds)) + " servers"))

@client.event
#Reaction roles
async def on_raw_reaction_add(ctx):
	user = ctx.member
	messageid = str(ctx.message_id)
	guild = user.guild
	emoji = ctx.emoji.name
	if user == client.user:
		return;
	else:
		if exists("rr/" + messageid):
			msgid = messageid
			channel = discord.utils.get(guild.channels, id=ctx.channel_id)
			message = await channel.fetch_message(msgid)
			info = open("rr/" + messageid,'r').read().split(",,")
			num = int(float(info[1]))
			x = 0
			while x < num:
				if info[x + 2].split("..")[0] == emoji:
					break
				x = x + 1
			print(str(x))
			role = info[x + 2].split("..")[1]
			role = message.guild.get_role(int(role))
			await user.add_roles(role)
		elif exists("livepoll/" + messageid):
			msgid = messageid
			channel = discord.utils.get(guild.channels, id=ctx.channel_id)
			msg = await channel.fetch_message(msgid)
			poll = msg.embeds[0]
			res = poll.fields
			qcount = len(res)
			trc = 0
			x = 0
			while x < qcount:
				trc = trc + msg.reactions[x].count - 1
				x = x + 1
			x = 0
			embed=discord.Embed(title="Live Poll", description=poll.description, color=0xffffff)
			while x < qcount:
				prc = int(round((msg.reactions[x].count-1)/trc*100))
				aa = round(prc/10)
				bb = 10 - round(prc/10)
				e = 0
				a = ""
				b = ""
				while e < aa:
					a = a + "▓"
					e = e + 1
				e = 0
				while e < bb:
					b = b + "░"
					e = e + 1
				embed.add_field(name=res[x].name.split(": ")[0] + ": " + res[x].name.split(": ")[1], value = a + b + " - " + str(prc) + "%", inline=False)
				x = x + 1
			embed.set_footer(text = "ID: " + str(msg.id))
			await msg.edit(embed = embed)

@client.event
async def on_raw_reaction_remove(ctx):
	guild_id = ctx.guild_id
	guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)
	user = await(await client.fetch_guild(ctx.guild_id)).fetch_member(ctx.user_id)
	messageid = str(ctx.message_id)
	emoji = ctx.emoji.name
	if user == client.user:
		return;
	else:
		if exists("rr/" + messageid):
			msgid = messageid
			channel = discord.utils.get(guild.channels, id=ctx.channel_id)
			message = await channel.fetch_message(msgid)
			info = open("rr/" + messageid,'r').read().split(",,")
			num = int(float(info[1]))
			x = 0
			while x < num:
				if info[x + 2].split("..")[0] == emoji:
					break
				x = x + 1
			print(str(x))
			role = info[x + 2].split("..")[1]
			role = message.guild.get_role(int(role))
			await user.remove_roles(role)
		elif exists("livepoll/" + messageid):
			msgid = messageid
			channel = discord.utils.get(guild.channels, id=ctx.channel_id)
			msg = await channel.fetch_message(msgid)
			poll = msg.embeds[0]
			res = poll.fields
			qcount = len(res)
			trc = 0
			x = 0
			while x < qcount:
				trc = trc + msg.reactions[x].count - 1
				x = x + 1
			x = 0
			embed=discord.Embed(title="Live Poll", description=poll.description, color=0xffffff)
			while x < qcount:
				if round(msg.reactions[x].count-1) > 0:
					prc = int(round((msg.reactions[x].count-1)/trc*100))
				else:
					prc = 0
				aa = round(prc/10)
				bb = 10 - round(prc/10)
				e = 0
				a = ""
				b = ""
				while e < aa:
					a = a + "▓"
					e = e + 1
				e = 0
				while e < bb:
					b = b + "░"
					e = e + 1
				embed.add_field(name=res[x].name.split(": ")[0] + ": " + res[x].name.split(": ")[1], value = a + b + " - " + str(prc) + "%", inline=False)
				x = x + 1
			embed.set_footer(text = "ID: " + str(msg.id))
			await msg.edit(embed = embed)


client.run("ODkxNjc5NDUxNDc2Mjc5MzA3.YVB3Mw.rW078ew6SY74I0pfMJHJBIWWZPI")



















