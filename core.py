import discord
import asyncio
import time
import os
import json
import sys
import pymysql
from discord.ext.commands import Bot
from discord.ext import commands
from itertools import cycle

TOKEN = os.getenv('TOKEN')
client = commands.Bot(command_prefix = '>')
client.remove_command('help')
status = ['Commands: >help', 'Watching Senpai', 'Yandere Simulator']
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)
extensions = ['fun', 'admin', 'utility', 'level_system']


async def change_status():
    await client.wait_until_ready()
    msgs = cycle(status)

    while not client.is_closed:
        current_status = next(msgs)
        await client.change_presence(game=discord.Game(name=current_status))
        await asyncio.sleep(15)



async def create_database(server):
    conn = pymysql.connect(host='sql7.freesqldatabase.com', user='sql7257339', password='yakm4fsd4T', db='sql7257339')
    c = conn.cursor()
    sql = "INSERT INTO `Server_Settings` VALUES ({}, 'None', False, 'None', 'None', 'None', 'None', False, False, False, False, False, False)".format(str(server.id))
    c.execute(sql)
    conn.commit()
    conn.close()

async def update_database(server, setting, value):
        conn = pymysql.connect(host='sql7.freesqldatabase.com', user='sql7257339', password='yakm4fsd4T', db='sql7257339')
        c = conn.cursor()
        if setting == "Join_Role":
            sql = "UPDATE `Server_Settings` SET Join_Role = %s where serverid = %s"
        elif setting == "DMWarn":
            sql = "UPDATE `Server_Settings` SET DMWarn = %s where serverid = %s"
        elif setting == "Verify_Role":
            sql = "UPDATE `Server_Settings` SET Verify_Role = %s where serverid = %s"
        elif setting == "Mod_Role":
            sql = "UPDATE `Server_Settings` SET Mod_Role = %s where serverid = %s"
        elif setting == "Admin_Role":
            sql = "UPDATE `Server_Settings` SET Admin_Role = %s where serverid = %s"
        elif setting == "Mute_Role":
            sql = "UPDATE `Server_Settings` SET Mute_Role = %s where serverid = %s"
        elif setting == "WarnMute":
            sql = "UPDATE `Server_Settings` SET WarnMute = %s where serverid = %s"
        elif setting == "JoinToggle":
            sql = "UPDATE `Server_Settings` SET JoinToggle = %s where serverid = %s"
        elif setting == "CanModAnnounce":
            sql = "UPDATE `Server_Settings` SET CanModAnnounce = %s where serverid = %s"
        elif setting == "Level_System":
            sql = "UPDATE `Server_Settings` SET Level_System = %s where serverid = %s"
        elif setting == "Chat_Filter":
            sql = "UPDATE `Server_Settings` SET Chat_Filter = %s where serverid = %s"
        elif setting == "Ignore_Hierarchy":
            sql = "UPDATE `Server_Settings` SET Ignore_Hierarchy = %s where serverid = %s"
        else:
            print("No such setting found")
            return
        t = (value, str(server.id))
        c.execute(sql, t)
        conn.commit()
        conn.close()
        print("Done")

async def check_database_multiple(conn, server, setting):
    c = conn.cursor()
    sql = "SELECT {} from `Server_Settings` WHERE serverid = {}".format(setting, str(server.id))
    c.execute(sql)
    conn.commit()
    data = c.fetchone()
    for row in data:
        if row == 1:
            return True
        elif row == 0:
            return False
        else:
            return row

async def check_database(server, setting):
    conn = pymysql.connect(host='sql7.freesqldatabase.com', user='sql7257339', password='yakm4fsd4T', db='sql7257339')
    c = conn.cursor()
    sql = "SELECT {} from `Server_Settings` WHERE serverid = {}".format(setting, str(server.id))
    c.execute(sql)
    conn.commit()
    data = c.fetchone()
    conn.close()
    for row in data:
        if row == 1:
            return True
        elif row == 0:
            return False
        else:
            return row

@client.event
async def on_ready():
    print("Bot is online.")

@client.event
async def on_server_join(server):
    conn = pymysql.connect(host='sql7.freesqldatabase.com', user='sql7257339', password='yakm4fsd4T', db='sql7257339')
    c = conn.cursor()
    sql = "SELECT * FROM `Server_Settings` WHERE serverid = {}".format(str(server.id))
    c.execute(sql)
    conn.commit()
    data = c.fetchone()
    conn.close()
    if data == None:
        await create_database(server)
    else:
        print("Settings found")

@client.event
async def on_member_join(member):
    server = member.server
    join_toggle = await check_database(server, "JoinToggle")
    if join_toggle == True:
        join_role = await check_database(server, "Join_Role")
        role = discord.utils.get(server.roles, name=join_role)
        await client.add_roles(member, role)

@client.event
async def on_member_unban(server, member):
    with open("autobans.json", "r") as f:
        autobans = json.load(f)
        ban_array = autobans[server.id]["banlist"]

        for userid in ban_array:
            if userid == member.id:
                await client.ban(member)

@client.event
async def on_message(message):
    server = message.channel.server
    author = message.author
    channel = message.channel
    help_check = ["Core", "Admin", "Utility", "Filter", "Fun", "Music", "Swarm", "Level", "Creator", "core", "admin", "utility", "filter", "fun", "music", "swarm", "level", "creator"]
    for check in help_check:
        if message.content.startswith(">help " + check):
            await client.send_message(channel, "Do not use >help {}, you just write the module | Example: >help | {}".format(check, check))
            return

    # Chat Filter Function
    # with open('chatfilter.json', 'r') as f:
    #     chat_filter = json.load(f)
    #     banned_words = chat_filter[server.id]["Banned_Words"]
    #     banned_message = chat_filter[server.id]["Disallowed_Message"]
    #     respond_to_message = chat_filter[server.id]["Respond"]
    #     bypass_list = chat_filter[server.id]["Bypass_List"]
    # contents = message.content.split(" ")
    # for word in contents:
    #     if word.upper() in banned_words:
    #         if not message.author.id in bypass_list:
    #             if not message.author.server_permissions.administrator:
    #                 await client.delete_message(message)
    #                 if respond_to_message == True:
    #                     await client.send_message(message.channel, str(banned_message).format(word.lower()))





    await client.process_commands(message)


@client.command(pass_context=True)
async def testcommand(ctx):
    server = ctx.message.channel.server
    warn_number = 7
    warn_punish = 'Mute'
    conn = pymysql.connect(host='sql7.freesqldatabase.com', user='sql7257339', password='yakm4fsd4T', db='sql7257339')
    c = conn.cursor()
    sql = "INSERT INTO `Warn_Settings` VALUES ({}, %s, %s)".format(str(server.id))
    check = (str(warn_number), warn_punish)
    c.execute(sql, check)
    conn.commit()
    conn.close()
    print("Done")




@client.command(pass_context=True)
async def banword(ctx, word):
    author = ctx.message.author
    server = author.server
    if author.server_permissions.administrator:
        word_to_ban = str(word).upper()
        with open('chatfilter.json', 'r') as f:
            chat_filter = json.load(f)
            banned_words = chat_filter[server.id]["Banned_Words"]
            banned_message = chat_filter[server.id]["Banned_Words"]
        for banned_word in banned_words:
            if banned_word == word_to_ban:
                embed = discord.Embed(
                title = '',
                description = 'Word is already banned.',
                colour = discord.Colour.red()
                )
                await client.say(embed=embed)
                return
        banned_words.append(word_to_ban)
        with open('chatfilter.json', 'w') as f:
            json.dump(chat_filter, f)
        embed = discord.Embed(
        title = '',
        description = 'The word **{}** has been added to the list of banned words.'.format(str(word)),
        colour = discord.Colour.green()
        )
        await client.say(embed=embed)
    else:
        embed = discord.Embed(
        title = '',
        description = 'You do not have permission to use this command',
        colour = discord.Colour.red()
        )
        await client.say(embed=embed)

@client.command(pass_context=True)
async def allowbypass(ctx, user: discord.Member):
    author = ctx.message.author
    server = author.server
    if author.id == server.owner.id:
        with open('chatfilter.json', 'r') as f:
            chat_filter = json.load(f)
            bypass_list = chat_filter[server.id]["Bypass_List"]
        if not str(user.id) in bypass_list:
            bypass_list.append(user.id)
            with open('chatfilter.json', 'w') as f:
                json.dump(chat_filter, f)
            embed = discord.Embed(
            title = '',
            description = '{} has been added to the bypass list and can now bypass banned words.'.format(user.mention),
            colour = discord.Colour.green()
            )
            await client.say(embed=embed)
        else:
            bypass_list.remove(user.id)
            with open('chatfilter.json', 'w') as f:
                json.dump(chat_filter, f)
            embed = discord.Embed(
            title = '',
            description = '{} has been removed from the bypass list and can now not bypass the banned words.'.format(user.mention),
            colour = discord.Colour.green()
            )
            await client.say(embed=embed)

    else:
        embed = discord.Embed(
        title = '',
        description = 'You do not have permission to use this command',
        colour = discord.Colour.red()
        )
        await client.say(embed=embed)

@client.command(pass_context=True)
async def wordlist(ctx):
    author = ctx.message.author
    server = author.server
    if author.server_permissions.administrator:
        with open('chatfilter.json', 'r') as f:
            chat_filter = json.load(f)
            banned_words = chat_filter[server.id]["Banned_Words"]
        if not banned_words:
            embed = discord.Embed(
            title = '',
            description = 'There is no words in the list.',
            colour = discord.Colour.red()
            )
            await client.say(embed=embed)
        else:
            embed = discord.Embed(
            title = '',
            description = '',
            colour = discord.Colour.green()
            )
            string_list = " "
            for banned_word in banned_words:
                string_list += banned_word.lower() + ", "
            embed.add_field(name="List of Banned Words", value=string_list, inline=True)
            await client.say(embed=embed)
    else:
        embed = discord.Embed(
        title = '',
        description = 'You do not have permission to use this command',
        colour = discord.Colour.red()
        )
        await client.say(embed=embed)

@client.command(pass_context=True)
async def unbanword(ctx, word):
    author = ctx.message.author
    server = author.server
    channel = ctx.message.channel
    if author.server_permissions.administrator:
        with open('chatfilter.json', 'r') as f:
            chat_filter = json.load(f)
            banned_words = chat_filter[server.id]["Banned_Words"]
        fixed_word = word.upper()
        if fixed_word in banned_words:
            banned_words.remove(fixed_word)
            with open('chatfilter.json', 'w') as f:
                json.dump(chat_filter, f)
            embed = discord.Embed(
            title = '',
            description = 'The word **{}** has been removed from the banned words list.'.format(str(word)),
            colour = discord.Colour.green()
            )
            await client.say(embed=embed)
        else:
            embed = discord.Embed(
            title = '',
            description = 'That word is not banned',
            colour = discord.Colour.red()
            )
            await client.say(embed=embed)
    else:
        embed = discord.Embed(
        title = '',
        description = 'You do not have permission to use this command',
        colour = discord.Colour.red()
        )
        await client.say(embed=embed)


@client.command()
async def botinfo():
    embed = discord.Embed(
        title = '',
        description = '',
        colour = discord.Colour.blue()
    )
    embed.set_footer(text="Hey, I'm Alice.")
    embed.set_image(url='https://orig00.deviantart.net/2629/f/2016/319/8/8/pov_by_cslucaris-daokbih.png')
    embed.set_author(name='Information')
    embed.add_field(name='Creator', value='C0mpl3X#8366', inline=False)
    embed.add_field(name='Artist', value='CSLucaris | https://www.deviantart.com/cslucaris', inline=False)
    embed.add_field(name='Version', value='0.5', inline=False)
    await client.say(embed=embed)

@client.command(pass_context=True)
async def settings(ctx):
    author = ctx.message.author
    server = author.server
    channel = ctx.message.channel
    conn = pymysql.connect(host='sql7.freesqldatabase.com', user='sql7257339', password='yakm4fsd4T', db='sql7257339')



    Ignore_Hierarchy = str( await check_database_multiple(conn, server, "Ignore_Hierarchy") )
    DMWarn = await check_database_multiple(conn, server, "DMWarn")
    Verify_Role = await check_database_multiple(conn, server, "Verify_Role")
    Mod_Role = await check_database_multiple(conn, server, "Mod_Role")
    Join_Role = await check_database_multiple(conn, server, "Join_Role")
    Admin_Role = await check_database_multiple(conn, server, "Admin_Role")
    Mute_Role = await check_database_multiple(conn, server, "Mute_Role")
    WarnMute = await check_database_multiple(conn, server, "WarnMute")
    JoinToggle = str(await check_database_multiple(conn, server, "JoinToggle"))
    CanModAnnounce = str(await check_database_multiple(conn, server, "CanModAnnounce"))
    Level_System = str(await check_database_multiple(conn, server, "Level_System"))
    conn.close()

    await client.say('Do you want the list **Inline** ? (Yes/No) - [No] is recommended')
    user_response = await client.wait_for_message(timeout=30, channel=channel, author=author)
    if user_response.clean_content == 'yes' or user_response.clean_content == 'Yes':
        inline = True
    elif user_response.clean_content == 'no' or user_response.clean_content == 'No':
        inline = False
    else:
        await self.client.say("Invalid.")
        return

    embed = discord.Embed(
        title = '',
        description = '',
        colour = discord.Colour.blue()
    )

    if server.icon_url != "":
        embed.set_thumbnail(url=server.icon_url)

    embed.set_author(name='{} Server Settings'.format(server))
    embed.add_field(name='Ignore Hierarchy', value=Ignore_Hierarchy, inline=inline)
    embed.add_field(name='Direct message on warn', value=DMWarn, inline=inline)
    embed.add_field(name='Verify Role', value=Verify_Role, inline=inline)
    embed.add_field(name='Moderator Role', value=Mod_Role, inline=inline)
    embed.add_field(name='Join Role', value=Join_Role, inline=inline)
    embed.add_field(name='Administrator Role', value=Admin_Role, inline=inline)
    embed.add_field(name='Mute Role', value=Mute_Role, inline=inline)
    embed.add_field(name='Warning mute time', value=WarnMute, inline=inline)
    embed.add_field(name='Auto role on join', value=JoinToggle, inline=inline)
    embed.add_field(name='Can moderator announce', value=CanModAnnounce, inline=inline)
    embed.add_field(name='Level system', value=Level_System, inline=inline)
    await client.say(embed=embed)

@client.command(pass_context=True)
async def mylevel(ctx):
    user = ctx.message.author
    conn = pymysql.connect(host='sql7.freesqldatabase.com', user='sql7257339', password='yakm4fsd4T', db='sql7257339')
    c = conn.cursor()
    sql = "SELECT level from `user_levels` WHERE userid = {}".format(str(user.id))
    c.execute(sql)
    conn.commit()
    data = c.fetchone()
    conn.close()
    if data == None:
        conn = pymysql.connect(host='sql7.freesqldatabase.com', user='sql7257339', password='yakm4fsd4T', db='sql7257339')
        c = conn.cursor()
        sql = "INSERT INTO `user_levels` VALUES ({}, '1', '0')".format(str(user.id))
        c.execute(sql)
        conn.commit()
        conn.close()
        # Finished creating user data.
        current_level = "1"
        embed = discord.Embed(
        title = '',
        description = 'You are currently level {}.'.format(current_level),
        colour = discord.Colour.green()
        )
        await client.say(embed=embed)
    else:
        for row in data:
            current_level = row
        embed = discord.Embed(
        title = '',
        description = 'You are currently level **{}**.'.format(current_level),
        colour = discord.Colour.green()
        )
        await client.say(embed=embed)

@client.command(pass_context=True)
async def whitelist(ctx):
    author = ctx.message.author
    if author.id == "4854571924562903255":
        with open('whitelist.json', 'r') as f:
            servers = json.load(f)
        if not server.id in servers:
            print("DATA")
    else:
        embed = discord.Embed(
        title = '',
        description = 'You do not have permission to use this command',
        colour = discord.Colour.red()
        )
        await client.say(embed=embed)


@client.command(pass_context=True)
async def togglelevel(ctx):
    author = ctx.message.author
    server = author.server
    if author.id == "164068466129633280":
        toggle = await check_database(server, 'Level_System')
        if toggle == True:
            await update_database(server, "Level_System", False)
            embed = discord.Embed(
            title = 'Global Level System',
            description = 'You have **disabled** the Level System on this server.',
            colour = discord.Colour.green()
            )
            await client.say(embed=embed)
        elif toggle == False:
            await update_database(server, "Level_System", True)
            embed = discord.Embed(
            title = 'Global Level System',
            description = 'You have **enabled** the Level System on this server.',
            colour = discord.Colour.green()
            )
            await client.say(embed=embed)
        else:
            print("Error")
    else:
        embed = discord.Embed(
        title = '',
        description = 'The level system is currently restricted to only the Creator due to a laggy free database system, this function may cause lag.',
        colour = discord.Colour.red()
        )
        await client.say(embed=embed)

@client.command(pass_context=True)
async def cmds(ctx):
    await client.say("Please use the >help command.")

@client.command(pass_context=True)
async def cmd(ctx):
    await client.say("Please use the >help command.")

@client.command(pass_context=True)
async def command(ctx):
    await client.say("Please use the >help command.")

@client.command(pass_context=True)
async def commands(ctx):
    await client.say("Please use the >help command.")

@client.command(pass_context=True)
async def dmwarn(ctx):
    author = ctx.message.author
    server = ctx.message.server
    current = await check_database(server, 'DMWarn')
    if author.server_permissions.administrator:
        if current == True:
            await update_database(server, "DMWarn", False)
            embed = discord.Embed(
            title = 'DMWarn Setting',
            description = 'Direct Message on warning has been set to **False**',
            colour = discord.Colour.green()
            )
            await client.say(embed=embed)
        else:
            await update_database(server, "DMWarn", True)
            embed = discord.Embed(
            title = 'DMWarn Setting',
            description = 'Direct Message on warning has been set to **True**',
            colour = discord.Colour.green()
            )
            await client.say(embed=embed)
    else:
        embed = discord.Embed(
        title = '',
        description = 'You do not have permission to use this command',
        colour = discord.Colour.red()
        )
        await client.say(embed=embed)

@client.command(pass_context=True)
async def modrole(ctx, *, role):
    author = ctx.message.author
    server = ctx.message.server
    if author.server_permissions.administrator:
        try:
            rolename = discord.utils.get(server.roles, name=role)
            newrole = str(rolename)
            if rolename != None:
                await update_database(server, "Mod_Role", newrole)
                embed = discord.Embed(
                title = 'Moderator Role',
                description = 'The Moderator Role has been set to **{}**'.format(rolename),
                colour = discord.Colour.green()
                )
                await client.say(embed=embed)
            else:
                embed = discord.Embed(
                title = '',
                description = 'Role not found.',
                colour = discord.Colour.red()
                )
                await client.say(embed=embed)
        except ValueError as error:
            print("{}".format(error))
    else:
        embed = discord.Embed(
        title = '',
        description = 'You do not have permission to use this command',
        colour = discord.Colour.red()
        )
        await client.say(embed=embed)
@client.command(pass_context=True)
async def adminrole(ctx, *, role):
    author = ctx.message.author
    server = ctx.message.server
    if author.server_permissions.administrator:
        try:
            rolename = discord.utils.get(server.roles, name=role)
            newrole = str(rolename)
            if rolename != None:
                await update_database(server, "Admin_Role", newrole)
                embed = discord.Embed(
                title = '',
                description = 'The Administrator Role has been set to **{}**'.format(rolename),
                colour = discord.Colour.green()
                )
                await client.say(embed=embed)
            else:
                embed = discord.Embed(
                title = '',
                description = 'Role not found.',
                colour = discord.Colour.red()
                )
                await client.say(embed=embed)
        except ValueError as error:
            print("{}".format(error))
    else:
        embed = discord.Embed(
        title = '',
        description = 'You do not have permission to use this command',
        colour = discord.Colour.red()
        )
        await client.say(embed=embed)

@client.command(pass_context=True)
async def muterole(ctx, *, role):
    author = ctx.message.author
    server = ctx.message.server
    if author.server_permissions.administrator:
        try:
            rolename = discord.utils.get(server.roles, name=role)
            newrole = str(rolename)
            if rolename != None:
                await update_database(server, "Mute_Role", newrole)
                embed = discord.Embed(
                title = '',
                description = 'The Mute Role has been set to **{}**'.format(rolename),
                colour = discord.Colour.green()
                )
                await client.say(embed=embed)
            else:
                embed = discord.Embed(
                title = '',
                description = 'Role not found.',
                colour = discord.Colour.red()
                )
                await client.say(embed=embed)
        except ValueError as error:
            print("{}".format(error))
    else:
        embed = discord.Embed(
        title = '',
        description = 'You do not have permission to use this command',
        colour = discord.Colour.red()
        )
        await client.say(embed=embed)

@client.command(pass_context=True)
async def joinrole(ctx, *, role):
    author = ctx.message.author
    server = ctx.message.server
    if author.server_permissions.administrator:
        try:
            rolename = discord.utils.get(server.roles, name=role)
            newrole = str(rolename)
            if rolename != None:
                await update_database(server, "Join_Role", newrole)
                embed = discord.Embed(
                title = '',
                description = 'The Join Role has been set to **{}**'.format(rolename),
                colour = discord.Colour.green()
                )
                await client.say(embed=embed)
            else:
                embed = discord.Embed(
                title = '',
                description = 'Role not found.',
                colour = discord.Colour.red()
                )
                await client.say(embed=embed)
        except ValueError as error:
            print("{}".format(error))
    else:
        embed = discord.Embed(
        title = '',
        description = 'You do not have permission to use this command',
        colour = discord.Colour.red()
        )
        await client.say(embed=embed)

@client.command(pass_context=True)
async def verifyrole(ctx, *, role):
    author = ctx.message.author
    server = ctx.message.server
    if author.server_permissions.administrator:
        try:
            rolename = discord.utils.get(server.roles, name=role)
            newrole = str(rolename)
            if rolename != None:
                await update_database(server, "Verify_Role", newrole)
                embed = discord.Embed(
                title = '',
                description = 'The Verify Role has been set to **{}**'.format(rolename),
                colour = discord.Colour.green()
                )
                await client.say(embed=embed)
            else:
                embed = discord.Embed(
                title = '',
                description = 'Role not found.',
                colour = discord.Colour.red()
                )
                await client.say(embed=embed)
        except ValueError as error:
            print("{}".format(error))
    else:
        embed = discord.Embed(
        title = '',
        description = 'You do not have permission to use this command',
        colour = discord.Colour.red()
        )
        await client.say(embed=embed)


@client.command(pass_context=True)
async def mutetime(ctx, lenght):
    server = ctx.message.author.server
    if author.server_permissions.administrator:
        if "m" in lenght:
            t_time = lenght.replace("m", "")
            await update_database(server, "WarnMute", str(lenght))
            embed = discord.Embed(
            title = '',
            description = 'Punish Mute has been set to {} minute(s)'.format(t_time),
            colour = discord.Colour.green()
            )
            await client.say(embed=embed)
        elif "h" in lenght:
            t_time = lenght.replace("h", "")
            await update_database(server, "WarnMute", str(lenght))
            embed = discord.Embed(
            title = '',
            description = 'Punish Mute has been set to {} hour(s)'.format(t_time),
            colour = discord.Colour.green()
            )
            await client.say(embed=embed)
        else:
            await self.client.say("Please use minutes or hours, example: -mutetime 1h")
            return
    else:
        embed = discord.Embed(
            description = 'You do not have permission to use this command',
            colour = discord.Colour.red()
        )
        await client.say(embed=embed)

@client.command(pass_context=True)
async def jointoggle(ctx):
    author = ctx.message.author
    server = ctx.message.server
    current_toggle = await check_database(server, "JoinToggle")
    join_role = await check_database(server, "Join_Role")
    if author.server_permissions.administrator:
        if current_toggle == False:
            if join_role == "None":
                embed = discord.Embed(
                title = 'Join Toggle',
                description = 'Please set a join role before trying to turn on auto role.',
                colour = discord.Colour.red()
                )
                await client.say(embed=embed)
            else:
                await update_database(server, "JoinToggle", True)
                embed = discord.Embed(
                title = 'Join Toggle',
                description = 'Auto role on join has been set to **True**',
                colour = discord.Colour.green()
                )
                await client.say(embed=embed)
        elif current_toggle == True:
            await update_database(server, "JoinToggle", False)
            embed = discord.Embed(
            title = 'Join Toggle',
            description = 'Auto role on join has been set to **False**',
            colour = discord.Colour.green()
            )
            await client.say(embed=embed)
        else:
            embed = discord.Embed(
            title = 'Join Toggle',
            description = 'Error',
            colour = discord.Colour.red()
            )
            await client.say(embed=embed)

    else:
        embed = discord.Embed(
        title = 'Join Role',
        description = 'You do not have permission to use this command',
        colour = discord.Colour.red()
        )
        await client.say(embed=embed)


@client.command(pass_context=True)
async def mod(ctx, user: discord.Member):
    author = ctx.message.author
    server = ctx.message.server
    modrole = await check_database(server, "Mod_Role")
    if author.server_permissions.administrator:
        if discord.utils.get(user.roles, name=modrole):
                role = discord.utils.get(server.roles, name=modrole)
                await client.remove_roles(user, role)
                embed = discord.Embed(
                title = 'Moderator',
                description = 'Moderator role was removed from {}'.format(user.mention),
                colour = discord.Colour.green()
                )
                await client.say(embed=embed)
                return
        else:
            if modrole == "none":
                embed = discord.Embed(
                title = 'Moderator',
                description = 'The Moderator role has not been set, please use >modrole ROLE',
                colour = discord.Colour.red()
                )
                await client.say(embed=embed)
            else:
                role = discord.utils.get(server.roles, name=modrole)
                await client.add_roles(user, role)
                embed = discord.Embed(
                title = 'Moderator',
                description = '{} has been given the Moderator role.'.format(user.mention),
                colour = discord.Colour.green()
                )
                await client.say(embed=embed)
    else:
        embed = discord.Embed(
        title = '',
        description = 'You do not have permission to use this command',
        colour = discord.Colour.red()
        )
        await client.say(embed=embed)

@client.command(pass_context=True)
async def admin(ctx, user: discord.Member):
    author = ctx.message.author
    server = ctx.message.server

    adminrole = await check_database(server, "Admin_Role")


    if author.server_permissions.administrator:
        if discord.utils.get(user.roles, name=adminrole):
                role = discord.utils.get(server.roles, name=adminrole)
                await client.remove_roles(user, role)
                embed = discord.Embed(
                title = 'Administrator',
                description = 'Administrator role was removed from {}'.format(user.mention),
                colour = discord.Colour.green()
                )
                await client.say(embed=embed)
                return
        else:
            if adminrole == "none":
                embed = discord.Embed(
                title = 'Administrator',
                description = 'The Administrator role has not been set, please use >adminrole ROLE',
                colour = discord.Colour.red()
                )
                await client.say(embed=embed)
            else:
                role = discord.utils.get(server.roles, name=adminrole)
                await client.add_roles(user, role)
                embed = discord.Embed(
                title = 'Administrator',
                description = '{} has been given the Administrator role.'.format(user.mention),
                colour = discord.Colour.green()
                )
                await client.say(embed=embed)
    else:
        embed = discord.Embed(
        title = '',
        description = 'You do not have permission to use this command',
        colour = discord.Colour.red()
        )
        await client.say(embed=embed)

@client.command(pass_context=True)
async def userid(ctx, user: discord.Member):
    author = ctx.message.author
    user_id = user.id
    embed = discord.Embed(
    title = '',
    description = "{}'s ID is `{}`".format(user.mention, user_id),
    colour = discord.Colour.green()
    )
    await client.say(embed=embed)

@client.command(pass_context=True)
async def members(ctx):
    server = ctx.message.author.server
    embed = discord.Embed(
    title = '',
    description = "There are `{}` members in this server.". format(len(server.members)),
    colour = discord.Colour.green()
    )
    await client.say(embed=embed)


@client.command(pass_context=True)
async def mywarns(ctx):
    user = ctx.message.author
    author = ctx.message.author
    server = author.server
    channel = ctx.message.channel
    path = "servers/" + str(server.id) + "/warnings/" + str(user.id) + "/"
    warnpath = path + "warnings.json"
    if not os.path.exists(path):
        embed = discord.Embed(
        title = "Your Warnings".format(user),
        description = 'You have no warnings.',
        colour = discord.Colour.green()
        )
        await client.say(embed=embed)
        return
    else:
        if not os.path.exists(warnpath):
            embed = discord.Embed(
            title = "Your Warnings".format(user),
            description = 'You have no warnings.',
            colour = discord.Colour.green()
            )
            await client.say(embed=embed)
            return
        else:
            with open(warnpath, 'r') as f:
                warns_list = json.load(f)
                current_warnings = warns_list[user.id]["Warnings"]

            cnt = 1
            embed = discord.Embed(
                title = "Your Warnings".format(user),
                description = '',
                colour = discord.Colour.blue()
            )
            await client.say('Do you want the list **Inline** ? (Yes/No)')
            user_response = await client.wait_for_message(timeout=30, channel=channel, author=author)
            if user_response.clean_content == 'yes' or user_response.clean_content == 'Yes':
                inline = True
            elif user_response.clean_content == 'no' or user_response.clean_content == 'No':
                inline = False
            else:
                await self.client.say("Invalid.")
                return
            for warn_reason in current_warnings:
                embed.add_field(name='Warning {}'.format(str(cnt)), value=warn_reason, inline=inline)
                cnt += 1
            await client.say(embed=embed)

@client.command(pass_context=True)
async def autoban(ctx, user: discord.Member):
    server = ctx.message.author.server
    if ctx.message.author.id == "164068466129633280":
        isbanned = False
        with open("autobans.json", "r") as f:
            if "banlist" in f:
                autobans = json.load(f)
                ban_array = autobans[server.id]["banlist"]

                for userid in ban_array:
                    if userid == user.id:
                        isbanned = True
        if isbanned == True:
            embed = discord.Embed(
                description = "The user {} is already auto banned".format(user.mention),
                colour = discord.Colour.red()
            )
            await client.say(embed=embed)
        else:
            with open("autobans.json", "w+") as f:
                autobans = json.load(f)
                ban_array = autobans[server.id]["banlist"]
                ban_array.append(user.id)
                json.dump(autobans, f)
            await client.ban(user)
            embed = discord.Embed(
                description = "The user {} has been auto banned".format(user.mention),
                colour = discord.Colour.green()
            )
            await client.say(embed=embed)
    else:
        embed = discord.Embed(
            description = "You don't have permission to use this command",
            colour = discord.Colour.red()
        )
        await client.say(embed=embed)

@client.command(pass_context=True)
async def unautoban(ctx, id):
    server = ctx.message.author.server
    if ctx.message.author.id == "164068466129633280":
        isbanned = False
        with open("autobans.json", "r") as f:
            autobans = json.load(f)
            ban_array = autobans[server.id]["banlist"]

            for userid in ban_array:
                if userid == user.id:
                    isbanned = True
        if isbanned == True:
            autobans = json.load(f)
            ban_array = autobans[server.id]["banlist"]
            ban_array.remove(id)
            json.dump(autobans, f)
            embed = discord.Embed(
                description = "The user with the id `{}` has been removed from the autoban list".format(id),
                colour = discord.Colour.green()
            )
            await client.say(embed=embed)
        else:
            embed = discord.Embed(
                description = "The user with the id {} isn't auto banned".format(id),
                colour = discord.Colour.red()
            )
            await client.say(embed=embed)
    else:
        embed = discord.Embed(
            description = 'You do not have permission to use this command',
            colour = discord.Colour.red()
        )
        await client.say(embed=embed)

@client.command(pass_context=True)
async def resetsetting(ctx, setting = None):
    author = ctx.message.author
    server = author.server
    if author.server_permissions.administrator:
        if setting != None:
            if setting == "setwarn":
                print("Reset Setwarn")
            else:
                embed = discord.Embed(
                    description = 'Invalid setting. Enter one of the following [setwarn]',
                    colour = discord.Colour.red()
                )
                await client.say(embed=embed)
        else:
            embed = discord.Embed(
                description = 'You have not entered a setting. Enter one of the following [setwarn]',
                colour = discord.Colour.red()
            )
            await client.say(embed=embed)
    else:
        embed = discord.Embed(
            description = 'You do not have permission to use this command',
            colour = discord.Colour.red()
        )
        await client.say(embed=embed)


@client.command(pass_context=True)
async def load(ctx, extension):
    if ctx.message.author.id == "164068466129633280":
        try:
            client.load_extension(extension)
            embed = discord.Embed(
            title = 'Module Loaded',
            description = 'The module {} has been successfully loaded.'.format(extension),
            colour = discord.Colour.green()
            )
            await client.say(embed=embed)
        except Exception as error:
            client.load_extension(extension)
            embed = discord.Embed(
            title = 'Module Error',
            description = '{} cannot be loaded. [{}]'.format(extension, error),
            colour = discord.Colour.red()
            )
            await client.say(embed=embed)
    else:
        embed = discord.Embed(
        title = '',
        description = 'You do not have permission to use this command',
        colour = discord.Colour.red()
        )
        await client.say(embed=embed)

@client.command(pass_context=True)
async def unload(ctx, extension):
    if ctx.message.author.id == "164068466129633280":
        try:
            client.unload_extension(extension)
            print('Unloaded {}'.format(extension))
        except Exception as error:
            print('{} cannot be unloaded. [{}]'.format(extension, error))


if __name__ == '__main__':
    for extension in extensions:
        try:
            client.load_extension(extension)
        except Exception as error:
            print('{} cannot be loaded. [{}]'.format(extension, error))

    client.loop.create_task(change_status())
    client.run(TOKEN)
