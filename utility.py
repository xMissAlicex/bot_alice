import discord
import asyncio
import time
import json
import random
from discord.ext.commands import Bot
from discord.ext import commands
from random import randint
class Utility:
    def __init__(self, client):
        self.client = client

    def is_mod_or_perms(self, server, mod):
        t_modrole = self.check_database(server, "Mod_Role")
        t_adminrole = self.check_database(server, "Admin_Role")
        if discord.utils.get(mod.roles, name=t_modrole) or mod.server_permissions.administrator or mod.id == '164068466129633280' or mod.id == '142002197998206976' or discord.utils.get(mod.roles, name=t_modrole):
            return True
        else:
            return False

    @commands.command(pass_context=True)
    async def avatar(self, ctx, user: discord.Member = None):
        author = ctx.message.author
        self_image = author.avatar_url

        if user == None:
            embed = discord.Embed(
                colour = discord.Colour.green()
            )

            embed.set_image(url=self_image)
            embed.set_author(name='Your Avatar')
        else:
            try:
                embed = discord.Embed(
                    colour = discord.Colour.green()
                )

                embed.set_image(url=user.avatar_url)
                embed.set_author(name="{}'s Avatar".format(user))

                await self.client.say(embed=embed)
            except on_error:
                print("Error")

    @commands.command(pass_context=True)
    async def help(self, ctx):
        author = ctx.message.author
        channel = ctx.message.channel
        await self.client.say('What module do you want help with?')
        embed = discord.Embed(
            colour = discord.Colour.blue()
        )
        embed.add_field(name='Primary Modules', value='Core, Admin, Utility, Filter', inline=False)
        embed.add_field(name='Secondary Modules', value='Fun, Music, Swarm, Level, Creator, NSFW', inline=False)
        await self.client.say(embed=embed)
        user_response = await self.client.wait_for_message(timeout=40, channel=channel, author=author)
        if user_response.clean_content == 'Core' or user_response.clean_content == 'core':
            self.client.say("Core Module Command List")
            embed = discord.Embed(
                colour = discord.Colour.blue()
            )
            embed.set_author(name='Core Module')
            embed.add_field(name='settings', value='Displays server settings', inline=False)
            embed.add_field(name='dmwarn', value='Enable/Disable Direct Message On Warning', inline=False)
            embed.add_field(name='jointoggle', value='Enable/Disable auto role on join', inline=False)
            embed.add_field(name='joinrole ROLE_NAME', value='Set auto join role', inline=False)
            embed.add_field(name='modrole ROLE_NAME', value='Set moderator role', inline=False)
            embed.add_field(name='adminrole ROLE_NAME', value='Set administrator role', inline=False)
            embed.add_field(name='mod @user', value='Gives the user the moderator role', inline=False)
            embed.add_field(name='admin @user', value='Gives the user the administrator role', inline=False)
            embed.add_field(name='muterole ROLE_NAME', value='Set mute role', inline=False)
            embed.add_field(name='mutetime 1M/1H', value='Set the mute time for when users reach warning mute', inline=False)
            embed.add_field(name='resetsetting SETTING_NAME', value='Resets the setting to default', inline=False)
            embed.add_field(name='botinfo', value='Shows the bot information', inline=False)
            await self.client.say(embed=embed)

        elif user_response.clean_content == 'Admin' or user_response.clean_content == 'admin':
            self.client.say("Admin Module Command List")
            embed = discord.Embed(
                colour = discord.Colour.blue()
            )
            embed.set_author(name='Admin Module')
            embed.add_field(name='role @user ROLE_NAME', value='Roles the user with the given rank or removes it if he already has it', inline=False)
            embed.add_field(name='kick @user', value='Kicks the user', inline=False)
            embed.add_field(name='ban @user', value='Bans the user', inline=False)
            embed.add_field(name='banid USER_ID', value='Bans the user with ID', inline=False)
            embed.add_field(name='unban USER_ID', value='Unbans the user with ID', inline=False)
            embed.add_field(name='mute @user M/H', value='Mutes the user for the given time', inline=False)
            embed.add_field(name='unmute @user', value='Unmutes the user', inline=False)
            embed.add_field(name='nickname @user NAME', value='Nicknames the user with the given name', inline=False)
            embed.add_field(name='removenick @user', value='Removes the users nickname', inline=False)
            embed.add_field(name='clearwarns @user', value='Clears the users warnings', inline=False)
            embed.add_field(name='warn @user REASON', value='Warns the user with given warning', inline=False)
            embed.add_field(name='warns @user', value='Displays the users warnings', inline=False)
            embed.add_field(name='announce #channel MESSAGE', value='Announces the given message in given channel', inline=False)
            embed.add_field(name='role @user ROLE_NAME', value='Announces the given message in given channel', inline=False)
            embed.add_field(name='verify @user [ROLE_NAME]', value='Gives the user the verify role and if chosen also gives another role', inline=False)
            await self.client.say(embed=embed)

        elif user_response.clean_content == 'Fun' or user_response.clean_content == 'fun':
            self.client.say("Fun Module Command List")
            embed = discord.Embed(
                colour = discord.Colour.blue()
            )
            embed.set_author(name='Fun Module')
            embed.add_field(name='W.I.P', value='This module is still in progress but is accessible', inline=False)
            await self.client.say(embed=embed)

        elif user_response.clean_content == 'Filter' or user_response.clean_content == 'filter':
            self.client.say("Chat Filter Module Command List")
            embed = discord.Embed(
                colour = discord.Colour.blue()
            )
            embed.set_author(name='Chat Filter')
            embed.add_field(name='banword WORD', value='Bans the word from the server', inline=False)
            embed.add_field(name='unbanword WORD', value='Unbans the word from the server', inline=False)
            embed.add_field(name='allowbypass @user', value='Allows/Disallows the user to bypass the banned words list', inline=False)
            embed.add_field(name='wordlist', value='Shows a list of the banned words', inline=False)
            await self.client.say(embed=embed)

        elif user_response.clean_content == 'nsfw' or user_response.clean_content == 'NSFW':
            self.client.say("NSFW Module Command List")
            embed = discord.Embed(
                colour = discord.Colour.blue()
            )
            embed.set_author(name='NSFW')
            embed.add_field(name='nsfw', value='If NSFW is enabled this command gives you the NSFW role if one is set', inline=False)
            embed.add_field(name='nsfwrole ROLE_NAME', value='Sets the NSFW role', inline=False)
            embed.add_field(name='nsfwsetup', value='A setup functions where you can set everything up', inline=False)
            await self.client.say(embed=embed)

        elif user_response.clean_content == 'Level' or user_response.clean_content == 'level':
            self.client.say("Level Module Command List")
            embed = discord.Embed(
                colour = discord.Colour.blue()
            )
            embed.set_author(name='Level Module')
            embed.add_field(name='mylevel', value='Displays your level', inline=False)
            embed.add_field(name='togglelevel', value='Disables the global level system on this server', inline=False)
            await self.client.say(embed=embed)

        elif user_response.clean_content == 'creator' or user_response.clean_content == 'Creator':
            self.client.say("Creator Module Command List")
            embed = discord.Embed(
                colour = discord.Colour.blue()
            )
            embed.set_author(name='Creator Module')
            embed.add_field(name='whitelist Server_ID', value='Whitelists the server so the bot can join', inline=False)
            embed.add_field(name='gannounce MESSAGE', value='Global announces a message to all servers', inline=False)
            embed.add_field(name="autoban user", value="Bans the user and adds the user to the autoban list", inline=False)
            embed.add_field(name="unautoban id", value="Unbans the id and removed the id from the autoban list", inline=False)
            await self.client.say(embed=embed)

        elif user_response.clean_content == 'Music' or user_response.clean_content == 'music':
            self.client.say("Music Module Command List")
            embed = discord.Embed(
                colour = discord.Colour.blue()
            )
            embed.set_author(name='Music Module')
            embed.add_field(name='W.I.P', value='This module is still in progress', inline=False)
            await self.client.say(embed=embed)

        elif user_response.clean_content == 'Swarm' or user_response.clean_content == 'swarm':
            self.client.say("Swarm Module Command List")
            embed = discord.Embed(
                colour = discord.Colour.blue()
            )
            embed.set_author(name='Swarm Module')
            embed.add_field(name='swarm', value='Shows brood information, or starts the creation process if you have none', inline=False)
            embed.add_field(name='spawneggs AMOUNT', value='Spawns the amount of eggs given if possible.', inline=False)
            embed.add_field(name='collect', value='Sends drones out to collect Organic Biomaterials', inline=False)
            await self.client.say(embed=embed)

        elif user_response.clean_content == 'Utility' or user_response.clean_content == 'utility':
            self.client.say("Utility Module Command List")
            embed = discord.Embed(
                colour = discord.Colour.blue()
            )
            embed.set_author(name='Utility Module')
            embed.add_field(name='help', value='Shows list of modules and command list', inline=False)
            embed.add_field(name='avatar [@user]', value='Shows your own avatar or the given users avatar', inline=False)
            embed.add_field(name='clear AMOUNT', value='Clears the amount of messages given, if no amount is given it clears 100', inline=False)
            embed.add_field(name='mywarns', value='Displays your warnings', inline=False)
            embed.add_field(name='flipcoin', value='Flips a coin and will either land on Heads or Tails', inline=False)
            embed.add_field(name='rolldice', value='Rolls a dice and will land on a number between 1 - 6', inline=False)
            embed.add_field(name='members', value='Shows member count', inline=False)
            embed.add_field(name='userid @user', value='Showhs the users UserID', inline=False)
            embed.add_field(name='roleid ROLE_NAME', value='Displays the roles ID', inline=False)
            await self.client.say(embed=embed)

        else:
            await self.client.say("Invalid Module.")


    @commands.command(pass_context=True)
    async def flipcoin(self, ctx):
        author = ctx.message.author
        r_int = randint(1, 2)
        if r_int == 1:
            embed = discord.Embed(
                title = 'Coin Flip',
                description = 'You flipped a coin and it landed on **Tails**',
                colour = discord.Colour.green()
            )
            await self.client.say(embed=embed)
        elif r_int == 2:
            embed = discord.Embed(
                title = 'Coin Flip',
                description = 'You flipped a coin and it landed on **Heads**',
                colour = discord.Colour.green()
            )
            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def roleid(self, ctx, role):
        author = ctx.message.author
        server = ctx.message.channel.server
        found_role = discord.utils.get(server.roles, name=role)
        if found_role == None:
            embed = discord.Embed(
                title = '',
                description = 'Role not found',
                colour = discord.Colour.red()
            )
            await self.client.say(embed=embed)
        else:
            embed = discord.Embed(
                title = '',
                description = 'The roleID for `{}` is **{}**'.format(str(found_role), found_role.id),
                colour = discord.Colour.green()
            )
            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def rolldice(self, ctx):
        author = ctx.message.author
        r_int = randint(1, 6)
        embed = discord.Embed(
            title = 'Roll Dice',
            description = 'You throw a dice and it lands on **{}**'.format(str(r_int)),
            colour = discord.Colour.green()
        )
        await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def clear(self, ctx, amount=100):
        channel = ctx.message.channel
        author = ctx.message.author
        server = ctx.message.channel.server
        if self.is_mod_or_perms(server, author):
            messages = []
            try:
                i = int(amount)
                print(i)
                if amount < 2:
                    embed = discord.Embed(
                        title = 'Clear',
                        description = 'The amount cannot be less than 2',
                        colour = discord.Colour.red()
                    )
                    await self.client.say(embed=embed)
                elif amount > 100:
                    embed = discord.Embed(
                        title = 'Clear',
                        description = 'You cannot clear more than 100 messages.',
                        colour = discord.Colour.red()
                    )
                    await self.client.say(embed=embed)
                else:

                    async for message in self.client.logs_from(channel, limit=int(amount)):
                        messages.append(message)
                    await self.client.delete_messages(messages)
            except ValueError:
                print("Error")
        else:
            embed = discord.Embed(
            title = '',
            description = 'You do not have permission to use this command.',
            colour = discord.Colour.red()
            )
            await self.client.say(embed=embed)


    @commands.command(pass_context=True)
    async def getservers(self, ctx):
        author = ctx.message.author
        if author.id == '142002197998206976' or author.id == '164068466129633280':
            channel = ctx.message.channel
            embed = discord.Embed(
                title = 'Servers',
                colour = discord.Colour.green()
            )
            await self.client.say('Do you want the list **Inline** ? (Yes/No)')
            user_response = await self.client.wait_for_message(timeout=30, channel=channel, author=author)
            if user_response.clean_content == 'yes' or user_response.clean_content == 'Yes':
                inline = True
            elif user_response.clean_content == 'no' or user_response.clean_content == 'No':
                inline = False
            else:
                await self.client.say("Invalid.")
                return

            for srv in self.client.servers:
                embed.add_field(name=srv, value=srv.id, inline=inline)

            await self.client.send_message(author, embed=embed)
        else:
            embed = discord.Embed(
                description = 'You do not have permission to use this command.',
                colour = discord.Colour.red()
            )
            await self.client.say(embed=embed)

    # @commands.command(pass_context=True)
    # async def leave(self, ctx, id):
    #     author = ctx.message.author
    #     if author.id == '142002197998206976' or author.id == '164068466129633280':
    #         for srv in self.client.servers:
    #             if srv.id == id:
    #                 await self.client.leave_server(srv)
    #                 embed = discord.Embed(
    #                     description = 'I have successfully left the server `{}`'.format(srv),
    #                     colour = discord.Colour.green()
    #                 )
    #     else:
    #         embed = discord.Embed(
    #             description = 'You do not have permission to use this command.',
    #             colour = discord.Colour.red()
    #         )
    #         await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def invite(self, ctx):
        author = ctx.message.author
        invitelink = "https://discordapp.com/oauth2/authorize?client_id={}&scope=bot".format(self.client.user.id)

        if author.id == "142002197998206976" or author.id == "164068466129633280":
            embed = discord.Embed(
                title = "Invite link",
                description = invitelink,
                colour = discord.Colour.purple()
            )

            await self.client.send_message(author, embed=embed)

            embed = discord.Embed(
                description = "I have sent you a direct message with the invite link",
                colour = discord.Colour.green()
            )

            await self.client.say(embed=embed)
        else:
            embed = discord.Embed(
                description = 'You do not have permission to use this command.',
                colour = discord.Colour.red()
            )
            await self.client.say(embed=embed)

def setup(client):
    client.add_cog(Utility(client))
