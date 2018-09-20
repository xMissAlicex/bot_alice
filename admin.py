import discord
import asyncio
import time
import os, sys
import pymysql
import json
from discord.ext.commands import Bot
from discord.ext import commands

class Admin:
    def __init__(self, client):
        self.client = client

    def check_database(self, server, setting):
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
    def check_warn_database(self, server, warnnumber):
        conn = pymysql.connect(host='sql7.freesqldatabase.com', user='sql7257339', password='yakm4fsd4T', db='sql7257339')
        c = conn.cursor()
        sql = "SELECT warn_number from `Warn_Settings` WHERE serverid = {}".format(str(server.id))
        c.execute(sql)
        conn.commit()
        data = c.fetchone()
        conn.close()
        print(str(data))
        for row in data:
            if row == str(warnnumber):
                return False
        return True




    def update_database(self, server, setting, value):
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
                sql = "UPDATE `Server_Settings` SET Chat_Filter = %s where serverid = %s"
            else:
                print("No such setting found")
                return
            t = (value, str(server.id))
            c.execute(sql, t)
            conn.commit()
            conn.close()
            print("Done")

    def is_allowed_by_hierarchy(self, server, mod, user):
        toggle = self.check_database(server, "Ignore_Hierarchy")
        special = mod == server.owner or mod.id == self.client.settings.owner
        if toggle == False:
            if mod.top_role.position > user.top_role.position:
                return False
            else:
                return True
        else:
            return True

    def is_mod_or_perms(self, server, mod):
        t_modrole = self.check_database(server, "Mod_Role")
        t_adminrole = self.check_database(server, "Admin_Role")
        if discord.utils.get(mod.roles, name=t_modrole) or mod.server_permissions.administrator or mod.id == '164068466129633280' or mod.id == '142002197998206976' or discord.utils.get(mod.roles, name=t_modrole):
            return True
        else:
            return False
    def is_admin_or_perms(self, server, mod):
        t_adminrole = self.check_database(server, "Admin_Role")
        if discord.utils.get(mod.roles, name=t_adminrole) or mod.server_permissions.administrator or mod.id == '164068466129633280' or mod.id == '142002197998206976':
            return True
        else:
            return False


    @commands.command(pass_context=True)
    async def warn(self, ctx, user: discord.Member, *, reason = "No Reason Given"):
        author = ctx.message.author
        server = author.server
        await self.client.say("Function currently down due to upgrading database system.")
        return
        if self.is_mod_or_perms(server, author):
            path = "servers/" + str(server.id) + "/warnings/" + str(user.id) + "/"
            if not os.path.exists(path):
                os.makedirs(path)
                warn_path = path + "warnings.json"
                if not os.path.exists(warn_path):
                    with open(warn_path, 'w+') as f:
                        json_data = {}
                        warnings = []
                        warnings.append(reason)
                        json_data[user.id] = {}
                        json_data[user.id]["Warnings"] = warnings
                        json.dump(json_data, f)
                        embed = discord.Embed(
                        title = '',
                        description = '{} has been warned with the reason **{}**'.format(user.mention, str(reason)),
                        colour = discord.Colour.green()
                        )
                        await self.client.say(embed=embed)

            else:
                warn_path = path + "warnings.json"
                if not os.path.exists(warn_path):
                    with open(warn_path, 'w+') as f:
                        json_data = {}
                        warnings = []
                        warnings.append(reason)
                        json_data[user.id] = {}
                        json_data[user.id]["Warnings"] = warnings
                        json.dump(json_data, f)
                        embed = discord.Embed(
                        title = '',
                        description = '{} has been warned with the reason **{}**'.format(user.mention, str(reason)),
                        colour = discord.Colour.green()
                        )
                        await self.client.say(embed=embed)
                else:
                    with open(warn_path, 'r') as f:
                        warns_list = json.load(f)
                        current_warnings = warns_list[user.id]["Warnings"]
                        current_warnings.append(reason)
                        warns_list[user.id]["Warnings"] = current_warnings


                        with open(warn_path, 'w') as f:
                            json.dump(warns_list, f)
                        embed = discord.Embed(
                        title = '',
                        description = '{} has been warned with the reason **{}**'.format(user.mention, str(reason)),
                        colour = discord.Colour.green()
                        )
                        await self.client.say(embed=embed)
                        #------------------------------------------------------------------

                               #
                               #
                               # with open('srv_settings.json', 'r') as f:
                               #     servers = json.load(f)
                               #     warn_time = self.check_database(server, "WarnMute")
                               #     muterole_name = servers[server.id]["Mute_Role"]
                               #     muterole = discord.utils.get(server.roles, name=muterole_name)
                               #
                               #
                               # if check_punish == "Mute":
                               #     if "m" in warn_time:
                               #         t_time = warn_time.replace("m", "")
                               #         time_type = "m"
                               #         if int(t_time) == 0:
                               #             time = 0
                               #         else:
                               #             time = int(t_time)*60
                               #     elif "h" in warn_time:
                               #         t_time = warn_time.replace("h", "")
                               #         time_type = "h"
                               #         if int(t_time) == 0:
                               #             time = 0
                               #         else:
                               #             time = int(t_time)*3600
                               #     user_roles = user.roles
                               #     path = "servers/" + str(server.id) + "/muted/"
                               #     if not os.path.exists(path):
                               #         os.makedirs(path)
                               #     mutepath = path + str(user.id) + ".txt"
                               #     f = open(mutepath, "w+")
                               #     for role in user_roles:
                               #         if str(role) != "@everyone":
                               #             usrole = str(role)
                               #             write = usrole + "\n"
                               #             f.write(write)
                               #     f.close()
                               #     print(user)
                               #     await self.client.replace_roles(user, muterole)
                               #     await asyncio.sleep(time)
                               #     path = "servers/" + str(server.id) + "/muted/" + str(user.id) + ".txt"
                               #     with open(path) as f:
                               #         line = fp.readline()
                               #         roles_to_give = []
                               #         while line:
                               #             role = discord.utils.get(server.roles, name=line.strip())
                               #             roles_to_give.append(role)
                               #             line = f.readline()
                               #         f.close()
                               #     await self.client.replace_roles(user, *roles_to_give)
                               #     os.remove(path)
                               #
                               # elif check_punish == "Kick":
                               #     await self.client.say("{} has been kicked for reaching the warning threshold.".format(user.mention))
                               #     await self.client.kick(user)
                               # elif check_punish == "Ban":
                               #     await self.client.say("{} has been banned for reaching the warning threshold.".format(user.mention))
                               #     await self.client.ban(user)
        else:
            embed = discord.Embed(
            title = '',
            description = 'You do not have permission to use this command.',
            colour = discord.Colour.red()
            )
            await self.client.say(embed=embed)



    @commands.command(pass_context=True)
    async def warnid(self, ctx, id, *, reason = "No Reason Given"):
        await self.client.say("Function currently down due to upgrading database system.")
        return
        # author = ctx.message.author
        # server = author.server
        # user = server.get_member(id)
        # if self.is_mod_or_perms(server, author):
        #     path = "servers/" + str(server.id) + "/warnings/" + str(user.id) + "/"
        #     if not os.path.exists(path):
        #         os.makedirs(path)
        #         warn_path = path + "warnings.json"
        #         if not os.path.exists(warn_path):
        #             with open(warn_path, 'w+') as f:
        #                 json_data = {}
        #                 warnings = []
        #                 warnings.append(reason)
        #                 json_data[user.id] = {}
        #                 json_data[user.id]["Warnings"] = warnings
        #                 json.dump(json_data, f)
        #                 embed = discord.Embed(
        #                 title = '',
        #                 description = '{} has been warned with the reason **{}**'.format(user.mention, str(reason)),
        #                 colour = discord.Colour.green()
        #                 )
        #                 await self.client.say(embed=embed)
        #
        #     else:
        #         warn_path = path + "warnings.json"
        #         if not os.path.exists(warn_path):
        #             with open(warn_path, 'w+') as f:
        #                 json_data = {}
        #                 warnings = []
        #                 warnings.append(reason)
        #                 json_data[user.id] = {}
        #                 json_data[user.id]["Warnings"] = warnings
        #                 json.dump(json_data, f)
        #                 embed = discord.Embed(
        #                 title = '',
        #                 description = '{} has been warned with the reason **{}**'.format(user.mention, str(reason)),
        #                 colour = discord.Colour.green()
        #                 )
        #                 await self.client.say(embed=embed)
        #         else:
        #             with open(warn_path, 'r') as f:
        #                 warns_list = json.load(f)
        #                 current_warnings = warns_list[user.id]["Warnings"]
        #                 current_warnings.append(reason)
        #                 warns_list[user.id]["Warnings"] = current_warnings
        #
        #
        #                 with open(warn_path, 'w') as f:
        #                     json.dump(warns_list, f)
        #                 embed = discord.Embed(
        #                 title = '',
        #                 description = '{} has been warned with the reason **{}**'.format(user.mention, str(reason)),
        #                 colour = discord.Colour.green()
        #                 )
        #                 await self.client.say(embed=embed)
        #                 #------------------------------------------------------------------
        #                 punish_path = "servers/" + str(server.id) + "/warn_punishments/"
        #                 t_path = punish_path + str(len(current_warnings)) + ".txt"
        #                 if os.path.exists(t_path):
        #                     with open(t_path) as fp:
        #                        line = fp.readline()
        #                        while line:
        #                            check_punish = line.strip()
        #                            line = fp.readline()
        #                        fp.close()
        #                        with open('srv_settings.json', 'r') as f:
        #                            servers = json.load(f)
        #                            warn_time = self.check_database(server, "WarnMute")
        #                            muterole_name = servers[server.id]["Mute_Role"]
        #                            muterole = discord.utils.get(server.roles, name=muterole_name)
        #
        #
        #                        if check_punish == "Mute":
        #                            if "m" in warn_time:
        #                                t_time = warn_time.replace("m", "")
        #                                time_type = "m"
        #                                if int(t_time) == 0:
        #                                    time = 0
        #                                else:
        #                                    time = int(t_time)*60
        #                            elif "h" in warn_time:
        #                                t_time = warn_time.replace("h", "")
        #                                time_type = "h"
        #                                if int(t_time) == 0:
        #                                    time = 0
        #                                else:
        #                                    time = int(t_time)*3600
        #                            user_roles = user.roles
        #                            path = "servers/" + str(server.id) + "/muted/"
        #                            if not os.path.exists(path):
        #                                os.makedirs(path)
        #                            mutepath = path + str(user.id) + ".txt"
        #                            f = open(mutepath, "w+")
        #                            for role in user_roles:
        #                                if str(role) != "@everyone":
        #                                    usrole = str(role)
        #                                    write = usrole + "\n"
        #                                    f.write(write)
        #                            f.close()
        #                            print(user)
        #                            await self.client.replace_roles(user, muterole)
        #                            await asyncio.sleep(time)
        #                            path = "servers/" + str(server.id) + "/muted/" + str(user.id) + ".txt"
        #                            with open(path) as f:
        #                                line = fp.readline()
        #                                roles_to_give = []
        #                                while line:
        #                                    role = discord.utils.get(server.roles, name=line.strip())
        #                                    roles_to_give.append(role)
        #                                    line = f.readline()
        #                                f.close()
        #                            await self.client.replace_roles(user, *roles_to_give)
        #                            os.remove(path)
        #
        #                        elif check_punish == "Kick":
        #                            await self.client.say("{} has been kicked for reaching the warning threshold.".format(user.mention))
        #                            await self.client.kick(user)
        #                        elif check_punish == "Ban":
        #                            await self.client.say("{} has been banned for reaching the warning threshold.".format(user.mention))
        #                            await self.client.ban(user)
        # else:
        #     embed = discord.Embed(
        #     title = '',
        #     description = 'You do not have permission to use this command.',
        #     colour = discord.Colour.red()
        #     )
        #     await self.client.say(embed=embed)


    @commands.command(pass_context=True)
    async def warnid(self, ctx, id, *, reason = "No Reason Given"):
        await self.client.say("Function currently down due to upgrading database system.")
        return
        # author = ctx.message.author
        # server = author.server
        # user = server.get_member(id)
        # if self.is_mod_or_perms(server, author):
        #     path = "servers/" + str(server.id) + "/warnings/" + str(user.id) + "/"
        #     if not os.path.exists(path):
        #         os.makedirs(path)
        #         warn_path = path + "warnings.json"
        #         if not os.path.exists(warn_path):
        #             with open(warn_path, 'w+') as f:
        #                 json_data = {}
        #                 warnings = []
        #                 warnings.append(reason)
        #                 json_data[user.id] = {}
        #                 json_data[user.id]["Warnings"] = warnings
        #                 json.dump(json_data, f)
        #                 embed = discord.Embed(
        #                 title = '',
        #                 description = '{} has been warned with the reason **{}**'.format(user.mention, str(reason)),
        #                 colour = discord.Colour.green()
        #                 )
        #                 await self.client.say(embed=embed)
        #
        #     else:
        #         warn_path = path + "warnings.json"
        #         if not os.path.exists(warn_path):
        #             with open(warn_path, 'w+') as f:
        #                 json_data = {}
        #                 warnings = []
        #                 warnings.append(reason)
        #                 json_data[user.id] = {}
        #                 json_data[user.id]["Warnings"] = warnings
        #                 json.dump(json_data, f)
        #                 embed = discord.Embed(
        #                 title = '',
        #                 description = '{} has been warned with the reason **{}**'.format(user.mention, str(reason)),
        #                 colour = discord.Colour.green()
        #                 )
        #                 await self.client.say(embed=embed)
        #         else:
        #             with open(warn_path, 'r') as f:
        #                 warns_list = json.load(f)
        #                 current_warnings = warns_list[user.id]["Warnings"]
        #                 current_warnings.append(reason)
        #                 warns_list[user.id]["Warnings"] = current_warnings
        #
        #
        #                 with open(warn_path, 'w') as f:
        #                     json.dump(warns_list, f)
        #                 embed = discord.Embed(
        #                 title = '',
        #                 description = '{} has been warned with the reason **{}**'.format(user.mention, str(reason)),
        #                 colour = discord.Colour.green()
        #                 )
        #                 await self.client.say(embed=embed)
        #                 #------------------------------------------------------------------
        #                 punish_path = "servers/" + str(server.id) + "/warn_punishments/"
        #                 t_path = punish_path + str(len(current_warnings)) + ".txt"
        #                 if os.path.exists(t_path):
        #                     with open(t_path) as fp:
        #                        line = fp.readline()
        #                        while line:
        #                            check_punish = line.strip()
        #                            line = fp.readline()
        #                        fp.close()
        #                        with open('srv_settings.json', 'r') as f:
        #                            servers = json.load(f)
        #                            warn_time = servers[server.id]["WarnMute"]
        #                            muterole_name = servers[server.id]["Mute_Role"]
        #                            muterole = discord.utils.get(server.roles, name=muterole_name)
        #
        #
        #                        if check_punish == "Mute":
        #                            if "m" in warn_time:
        #                                t_time = warn_time.replace("m", "")
        #                                time_type = "m"
        #                                if int(t_time) == 0:
        #                                    time = 0
        #                                else:
        #                                    time = int(t_time)*60
        #                            elif "h" in warn_time:
        #                                t_time = warn_time.replace("h", "")
        #                                time_type = "h"
        #                                if int(t_time) == 0:
        #                                    time = 0
        #                                else:
        #                                    time = int(t_time)*3600
        #                            user_roles = user.roles
        #                            path = "servers/" + str(server.id) + "/muted/"
        #                            if not os.path.exists(path):
        #                                os.makedirs(path)
        #                            mutepath = path + str(user.id) + ".txt"
        #                            f = open(mutepath, "w+")
        #                            for role in user_roles:
        #                                if str(role) != "@everyone":
        #                                    usrole = str(role)
        #                                    write = usrole + "\n"
        #                                    f.write(write)
        #                            f.close()
        #                            print(user)
        #                            await self.client.replace_roles(user, muterole)
        #                            await asyncio.sleep(time)
        #                            path = "servers/" + str(server.id) + "/muted/" + str(user.id) + ".txt"
        #                            with open(path) as f:
        #                                line = fp.readline()
        #                                roles_to_give = []
        #                                while line:
        #                                    role = discord.utils.get(server.roles, name=line.strip())
        #                                    roles_to_give.append(role)
        #                                    line = f.readline()
        #                                f.close()
        #                            await self.client.replace_roles(user, *roles_to_give)
        #                            os.remove(path)
        #
        #                        elif check_punish == "Kick":
        #                            await self.client.say("{} has been kicked for reaching the warning threshold.".format(user.mention))
        #                            await self.client.kick(user)
        #                        elif check_punish == "Ban":
        #                            await self.client.say("{} has been banned for reaching the warning threshold.".format(user.mention))
        #                            await self.client.ban(user)
        # else:
        #     embed = discord.Embed(
        #     title = '',
        #     description = 'You do not have permission to use this command.',
        #     colour = discord.Colour.red()
        #     )
        #     await self.client.say(embed=embed)


    @commands.command(pass_context=True)
    async def warns(self, ctx, user: discord.Member):
        await self.client.say("Function currently down due to upgrading database system.")
        return
        # author = ctx.message.author
        # server = author.server
        # channel = ctx.message.channel
        # path = "servers/" + str(server.id) + "/warnings/" + str(user.id) + "/"
        # warnpath = path + "warnings.json"
        # if not os.path.exists(path):
        #     embed = discord.Embed(
        #     title = "{} Warnings".format(user),
        #     description = 'This user has no warnings.',
        #     colour = discord.Colour.green()
        #     )
        #     await self.client.say(embed=embed)
        #     return
        # else:
        #     if not os.path.exists(warnpath):
        #         embed = discord.Embed(
        #         title = "{} Warnings".format(user),
        #         description = 'This user has no warnings.',
        #         colour = discord.Colour.green()
        #         )
        #         await self.client.say(embed=embed)
        #         return
        #     else:
        #         with open(warnpath, 'r') as f:
        #             warns_list = json.load(f)
        #             current_warnings = warns_list[user.id]["Warnings"]
        #
        #         cnt = 1
        #         embed = discord.Embed(
        #             title = "{} Warnings".format(user),
        #             description = '',
        #             colour = discord.Colour.blue()
        #         )
        #         await self.client.say('Do you want the list **Inline** ? (Yes/No)')
        #         user_response = await self.client.wait_for_message(timeout=30, channel=channel, author=author)
        #         if user_response.clean_content == 'yes' or user_response.clean_content == 'Yes':
        #             inline = True
        #         elif user_response.clean_content == 'no' or user_response.clean_content == 'No':
        #             inline = False
        #         else:
        #             await self.client.say("Invalid.")
        #             return
        #         for warn_reason in current_warnings:
        #             embed.add_field(name='Warning {}'.format(str(cnt)), value=warn_reason, inline=inline)
        #             cnt += 1
        #         await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def clearwarns(self, ctx, user: discord.Member):
        await self.client.say("Function currently down due to upgrading database system.")
        return
        # server = ctx.message.author.server
        # author = ctx.message.author
        # if self.is_admin_or_perms(server, author):
        #     path = "servers/" + str(server.id) + "/warnings/" + str(user.id) + "/"
        #     warnpath = path + "warnings.json"
        #     os.remove(warnpath)
        #     embed = discord.Embed(
        #     title = '',
        #     description = "{} Warnings has been removed.".format(user.mention),
        #     colour = discord.Colour.green()
        #     )
        #     await self.client.say(embed=embed)
        # else:
        #     embed = discord.Embed(
        #     title = '',
        #     description = 'You do not have permission to use this command.',
        #     colour = discord.Colour.red()
        #     )
        #     await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def verify(self, ctx, user: discord.Member, *, role_name = None):
        author = ctx.message.author
        server = author.server
        if self.is_admin_or_perms(server, author):
            verifyrole_name = self.check_database(server, "Verify_Role")
            verifyrole = discord.utils.get(server.roles, name=verifyrole_name)
            if role_name == None:
                if verifyrole != None:
                    await self.client.add_roles(user, verifyrole)
                    embed = discord.Embed(
                    title = '',
                    description = '{} has been verified'.format(user.mention),
                    colour = discord.Colour.green()
                    )
                    await self.client.say(embed=embed)
                else:
                    embed = discord.Embed(
                    title = '',
                    description = 'There is no Verify Role set, please use -verifyrole ROLE_NAME',
                    colour = discord.Colour.red()
                    )
                    await self.client.say(embed=embed)
            else:
                extra_role = discord.utils.get(server.roles, name=role_name)
                if extra_role != None:
                    roles_to_give = []
                    roles_to_give.append(verifyrole)
                    roles_to_give.append(extra_role)
                    await self.client.add_roles(user, *roles_to_give)
                    embed = discord.Embed(
                    title = '',
                    description = '{} has been verified and given the role **{}**'.format(user.mention, role_name),
                    colour = discord.Colour.green()
                    )
                    await self.client.say(embed=embed)
                else:
                    embed = discord.Embed(
                    title = '',
                    description = '**{}** role was not found'.format(role_name),
                    colour = discord.Colour.red()
                    )
                    await self.client.say(embed=embed)

                print("WITH ROLE")

        else:
            embed = discord.Embed(
            title = '',
            description = 'You do not have permission to use this command.',
            colour = discord.Colour.red()
            )
            await self.client.say(embed=embed)


    @commands.command(pass_context=True)
    async def setwarn(self, ctx, warn_number, punishment):
        author = ctx.message.author
        server = author.server
        if author == server.owner or author.id == 164068466129633280:
            if punishment == "mute" or punishment == "Mute":
                t_punish = 'Mute'
            elif punishment == "kick" or punishment == "Kick":
                t_punish = 'Kick'
            elif punishment == "ban" or punishment == "Ban":
                t_punish = 'Ban'
            else:
                self.client.say("That is not a possible punishment, the possible punishments is [Mute/Kick/Ban]")
                return
            if self.check_warn_database(server, str(warn_number)):
                conn = pymysql.connect(host='sql7.freesqldatabase.com', user='sql7257339', password='yakm4fsd4T', db='sql7257339')
                c = conn.cursor()
                sql = "INSERT INTO `Warn_Settings` VALUES ({}, %s, %s)".format(str(server.id))
                check = (str(warn_number), t_punish)
                c.execute(sql, check)
                conn.commit()
                conn.close()
                embed = discord.Embed(
                title = '',
                description = 'The punishment for warn number **{}** has been set to **{}**'.format(str(warn_number), t_punish),
                colour = discord.Colour.green()
                )
                await self.client.say(embed=embed)
            else:
                print("Error")
        else:
            embed = discord.Embed(
            title = '',
            description = 'You do not have permission to use this command.',
            colour = discord.Colour.red()
            )
            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def nickname(self, ctx, user: discord.Member, *, nick):
        author = ctx.message.author
        server = author.server
        if self.is_mod_or_perms(server, author):
            try:
                await self.client.change_nickname(user, nick)
                embed = discord.Embed(
                title = '',
                description = "Changed {}'s nickname to **{}**".format(user.mention, nick),
                colour = discord.Colour.green()
                )
                await self.client.say(embed=embed)
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
    async def removenick(self, ctx, user: discord.Member):
        author = ctx.message.author
        server = author.server
        if self.is_mod_or_perms(server, author):
            await self.client.change_nickname(user, None)
            embed = discord.Embed(
            title = '',
            description = "Removed {}'s nickname.".format(user.mention),
            colour = discord.Colour.green()
            )
            await self.client.say(embed=embed)
        else:
            embed = discord.Embed(
            title = '',
            description = 'You do not have permission to use this command.',
            colour = discord.Colour.red()
            )
            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def announce(self, ctx, u_channel: discord.Channel, *, message = None):
        author = ctx.message.author
        server = ctx.message.server
        channel = ctx.message.channel
        if message == None:
            await self.client.say("Please type a message")
            return
        ModAllowed = self.check_database(server, "CanModAnnounce")
        if ModAllowed == False:
            if self.is_mod_or_perms(server, author):
                embed = discord.Embed(
                title = '',
                description = 'Who do you wish to tag? [everyone / here / None]',
                colour = discord.Colour.orange()
                )
                await self.client.send_message(channel, embed=embed)
                user_response = await self.client.wait_for_message(timeout=30, channel=channel, author=author)
                if user_response.clean_content == 'everyone' or user_response.clean_content == 'Everyone':
                    embed = discord.Embed(
                    title = '',
                    description = 'Do you want your message to be inside an embed? (Yes/No)',
                    colour = discord.Colour.orange()
                    )
                    await self.client.send_message(channel, embed=embed)
                    user_response2 = await self.client.wait_for_message(timeout=30, channel=channel, author=author)
                    if user_response2.clean_content == 'Yes' or user_response2.clean_content == 'yes':
                        embed = discord.Embed(
                        title = '',
                        description = '{}'.format(str(message)),
                        colour = discord.Colour.orange()
                        )
                        embed.set_author(name=author.name, icon_url=author.avatar_url)
                        await self.client.send_message(u_channel, "@everyone")
                        await self.client.send_message(u_channel, embed=embed)
                    elif user_response2.clean_content == 'No' or user_response2.clean_content == 'no':
                        await self.client.send_message(u_channel, "@everyone")
                        await self.client.send_message(u_channel, str(message))
                    else:
                        await self.client.say("Invalid.")
                        return
                elif user_response.clean_content == 'here' or user_response.clean_content == 'Here':
                    embed = discord.Embed(
                    title = '',
                    description = 'Do you want your message to be inside an embed? (Yes/No)',
                    colour = discord.Colour.orange()
                    )
                    await self.client.send_message(channel, embed=embed)
                    user_response2 = await self.client.wait_for_message(timeout=30, channel=channel, author=author)
                    if user_response2.clean_content == 'Yes' or user_response2.clean_content == 'yes':
                        embed = discord.Embed(
                        title = '',
                        description = '{}'.format(str(message)),
                        colour = discord.Colour.orange()
                        )
                        embed.set_author(name=author.name, icon_url=author.avatar_url)
                        await self.client.send_message(u_channel, "@here")
                        await self.client.send_message(u_channel, embed=embed)
                    elif user_response2.clean_content == 'No' or user_response2.clean_content == 'no':
                        await self.client.send_message(u_channel, "@here")
                        await self.client.send_message(u_channel, str(message))
                    else:
                        await self.client.say("Invalid.")
                        return
                elif user_response.clean_content == 'None' or user_response.clean_content == 'none':
                    embed = discord.Embed(
                    title = '',
                    description = 'Do you want your message to be inside an embed? (Yes/No)',
                    colour = discord.Colour.orange()
                    )
                    await self.client.send_message(channel, embed=embed)
                    user_response2 = await self.client.wait_for_message(timeout=30, channel=channel, author=author)
                    if user_response2.clean_content == 'Yes' or user_response2.clean_content == 'yes':
                        embed = discord.Embed(
                        title = '',
                        description = '{}'.format(str(message)),
                        colour = discord.Colour.orange()
                        )
                        embed.set_author(name=author.name, icon_url=author.avatar_url)
                        await self.client.send_message(u_channel, embed=embed)
                    elif user_response2.clean_content == 'No' or user_response2.clean_content == 'no':
                        await self.client.send_message(u_channel, str(message))
                    else:
                        await self.client.say("Invalid.")
                        return
                else:
                    await self.client.say("Invalid.")
                    return

            else:
                embed = discord.Embed(
                title = 'Permission Denied',
                description = 'You do not have permission to use this command {}'.format(ctx.message.author.mention),
                colour = discord.Colour.red()
                )

                await client.send_message(channel, embed=embed)

        elif ModAllowed == True:
            print("no")
        else:
            print("Error")


    @commands.command(pass_context=True)
    async def kick(self, ctx, user: discord.Member, *, reason = None):
        author = ctx.message.author
        server = author.server
        if self.is_admin_or_perms(server, author):
            if author == user:
                embed = discord.Embed(
                title = 'Kick',
                description = 'You cannot kick youself.',
                colour = discord.Colour.red()
                )
                await self.client.say(embed=embed)
                return

            elif self.is_allowed_by_hierarchy(server, author, user):
                embed = discord.Embed(

                title = 'Kick',
                description = 'You cannot kick somebody higher than youself.',
                colour = discord.Colour.red()
                )
                await self.client.say(embed=embed)
                return
            try:
                await self.client.kick(user)
                if reason == None:
                    embed = discord.Embed(
                        title = 'User Kicked',
                        description = '',
                        colour = discord.Colour.blue()
                    )
                    embed.set_author(name='Mr. X', icon_url='https://cdn.discordapp.com/avatars/472817090785705985/b5318faf95792ae0a80ddb2e117e7ab7.png?size=128')
                    embed.add_field(name='User', value=user, inline=False)
                    await self.client.say(embed=embed)
                    await self.client.send_message(user, "You have been kicked from {}".format(server))
                else:
                    embed = discord.Embed(
                        title = 'User Kicked',
                        description = '',
                        colour = discord.Colour.blue()
                    )
                    embed.set_author(name='Mr. X', icon_url='https://cdn.discordapp.com/avatars/472817090785705985/b5318faf95792ae0a80ddb2e117e7ab7.png?size=128')
                    embed.add_field(name='User', value=user, inline=False)
                    embed.add_field(name='Reason', value=reason, inline=False)
                    await self.client.say(embed=embed)
                    await self.client.send_message(user, "You have been kicked from `{}` for the reason `{}`".format(server, reason))
            except discord.Forbidden:
                embed = discord.Embed(
                title = 'Kick',
                description = 'I do not have permissions to kick that user.',
                colour = discord.Colour.red()
                )
                await self.client.say(embed=embed)
            except Exception as e:
                print(e)
        else:
            embed = discord.Embed(
            title = '',
            description = 'You do not have permission to use this command.',
            colour = discord.Colour.red()
            )
            await self.client.say(embed=embed)
    @commands.command(pass_context=True)
    async def ban(self, ctx, user: discord.Member, *, reason = None):
        author = ctx.message.author
        server = ctx.message.server
        if self.is_admin_or_perms(server, author):
            if author == user:
                embed = discord.Embed(
                title = 'ban',
                description = 'You cannot ban youself.',
                colour = discord.Colour.red()
                )
                await self.client.say(embed=embed)
                return

            elif self.is_allowed_by_hierarchy(server, author, user):
                embed = discord.Embed(
                title = 'Ban',
                description = 'You cannot ban somebody higher than youself.',
                colour = discord.Colour.red()
                )
                await self.client.say(embed=embed)
                return

            try:
                await self.client.ban(user)
                if reason == None:
                    embed = discord.Embed(
                        title = 'User Banned',
                        description = '',
                        colour = discord.Colour.blue()
                    )
                    embed.set_author(name='Mr. X', icon_url='https://cdn.discordapp.com/avatars/472817090785705985/b5318faf95792ae0a80ddb2e117e7ab7.png?size=128')
                    embed.add_field(name='User', value=user, inline=False)
                    await self.client.say(embed=embed)
                    await self.client.send_message(user, 'You have been banned from `{}`'.format(server))
                else:
                    embed = discord.Embed(
                        title = 'User Banned',
                        description = '',
                        colour = discord.Colour.blue()
                    )
                    embed.set_author(name='Mr. X', icon_url='https://cdn.discordapp.com/avatars/472817090785705985/b5318faf95792ae0a80ddb2e117e7ab7.png?size=128')
                    embed.add_field(name='User', value=user, inline=False)
                    embed.add_field(name='Reason', value=reason, inline=False)
                    await self.client.say(embed=embed)
                    await self.client.send_message(user, 'You have been banned from `{}` for the reason `{}`'.format(server, reason))
            except discord.Forbidden:
                await self.client.kick(user)
                embed = discord.Embed(
                title = 'Ban',
                description = 'I do not have permissions to ban that user.',
                colour = discord.Colour.red()
                )
                await self.client.say(embed=embed)
            except Exception as e:
                print(e)
        else:
            embed = discord.Embed(
            title = '',
            description = 'You do not have permission to use this command.',
            colour = discord.Colour.red()
            )
            await self.client.say(embed=embed)
    @commands.command(pass_context=True)
    async def banid(self, ctx, id):
        is_id = False
        author = ctx.message.author
        server = ctx.message.server
        if self.is_admin_or_perms(server, author):
            try:
                int(id)
                is_id = True
            except ValueError:
                is_id = False

            if is_id:
                if author.server_permissions.ban_members:
                    await self.client.ban(server.get_member(id))
                    embed = discord.Embed(
                    title = 'banid',
                    description = 'The user with the id {} has been banned'.format(id),
                    colour = discord.Colour.green()
                    )
                    await self.client.say(embed=embed)
                else:
                    embed = discord.Embed(
                    title = 'banid',
                    description = 'You do not have the required permissions.',
                    colour = discord.Colour.green()
                    )
                    await self.client.say(embed=embed)
            else:
                embed = discord.Embed(
                title = 'banid',
                description = 'Please enter a userID.',
                colour = discord.Colour.red()
                )
                await self.client.say(embed=embed)
        else:
            embed = discord.Embed(
            title = '',
            description = 'You do not have permission to use this command.',
            colour = discord.Colour.red()
            )
            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def unban(self, ctx, userID):
        author = ctx.message.author
        server = author.server
        if author.server_permissions.ban:
            self.client.unban(server, userID)

    @commands.command(pass_context=True)
    async def mute(self, ctx, user: discord.Member, lenght = "0m"):
        author = ctx.message.author
        server = author.server
        if self.is_mod_or_perms(server, author):
            if "m" in lenght:
                print("He wrote it in minutes")
                t_time = lenght.replace("m", "")
                time_type = "m"
                if int(t_time) == 0:
                    time = 0
                else:
                    time = int(t_time)*60

            elif "h" in lenght:
                t_time = lenght.replace("h", "")
                time_type = "h"
                if int(t_time) == 0:
                    time = 0
                else:
                    time = int(t_time)*3600
            else:
                await self.client.say("Please use minutes or hours, example: -mute @user 20m")
                return
            get_role = self.check_database(server, "Mute_Role")
            mutedrole = discord.utils.get(server.roles, name=get_role)
            if mutedrole == None:
                await self.client.say("No mute role is set, please use >muterole ROLE_NAME")
                return
            userroles = user.roles
            path = "servers/" + str(server.id) + "/muted/"
            if not os.path.exists(path):
                os.makedirs(path)
                await self.client.say("Mute Folder was made")
            mutepath = path + str(user.id) + ".txt"
            f = open(mutepath, "w+")
            for role in userroles:
                if str(role) != "@everyone":
                    usrole = str(role)
                    write = usrole + "\n"
                    f.write(write)
            f.close()
            await self.client.replace_roles(user, mutedrole)
            if time != 0:
                if time_type == "m":
                    embed = discord.Embed(
                    title = '',
                    description = '{} Has been muted for {} minute(s)'.format(user.mention, str(t_time)),
                    colour = discord.Colour.green()
                    )
                    await self.client.say(embed=embed)
                    await asyncio.sleep(time)
                    path = "servers/" + str(server.id) + "/muted/" + str(user.id) + ".txt"
                    with open(path) as fp:
                       line = fp.readline()
                       roles_to_give = []
                       while line:
                           role = discord.utils.get(server.roles, name=line.strip())
                           roles_to_give.append(role)
                           line = fp.readline()
                       fp.close()
                    await self.client.replace_roles(user, *roles_to_give)
                    embed = discord.Embed(
                    title = '',
                    description = '{} Has been unmuted.'.format(user.mention),
                    colour = discord.Colour.green()
                    )
                    await self.client.say(embed=embed)
                    os.remove(path)
                elif time_type == "h":
                    embed = discord.Embed(
                    title = '',
                    description = '{} Has been muted for {} hour(s)'.format(user.mention, str(t_time)),
                    colour = discord.Colour.green()
                    )
                    await self.client.say(embed=embed)
                    await asyncio.sleep(time)
                    path = "servers/" + str(server.id) + "/muted/" + str(user.id) + ".txt"
                    with open(path) as fp:
                       line = fp.readline()
                       roles_to_give = []
                       while line:
                           role = discord.utils.get(server.roles, name=line.strip())
                           roles_to_give.append(role)
                           line = fp.readline()
                       fp.close()
                    await self.client.replace_roles(user, *roles_to_give)
                    embed = discord.Embed(
                    title = '',
                    description = '{} Has been unmuted.'.format(user.mention),
                    colour = discord.Colour.green()
                    )
                    await self.client.say(embed=embed)
                    os.remove(path)

            else:
                embed = discord.Embed(
                title = '',
                description = '{} Has been muted.'.format(user.mention),
                colour = discord.Colour.green()
                )
                await self.client.say(embed=embed)
        else:
            embed = discord.Embed(
            title = '',
            description = 'You do not have permission to use this command.',
            colour = discord.Colour.red()
            )
            await self.client.say(embed=embed)


    @commands.command(pass_context=True)
    async def muteid(self, ctx, userID, lenght = "0m"):
        author = ctx.message.author
        server = author.server
        if self.is_mod_or_perms(server, author):
            user = server.get_member(userID)
            if "m" in lenght:
                print("He wrote it in minutes")
                t_time = lenght.replace("m", "")
                time_type = "m"
                if int(t_time) == 0:
                    time = 0
                else:
                    time = int(t_time)*60

            elif "h" in lenght:
                t_time = lenght.replace("h", "")
                time_type = "h"
                if int(t_time) == 0:
                    time = 0
                else:
                    time = int(t_time)*3600
            else:
                await self.client.say("Please use minutes or hours, example: -mute userID 20m")
                return
            get_role = self.check_database(server, "Mute_Role")
            mutedrole = discord.utils.get(server.roles, name=get_role)
            if mutedrole == None:
                await self.client.say("No mute role is set, please use >muterole ROLE_NAME")
                return
            userroles = user.roles
            path = "servers/" + str(server.id) + "/muted/"
            if not os.path.exists(path):
                os.makedirs(path)
                await self.client.say("Mute Folder was made")
            mutepath = path + str(user.id) + ".txt"
            f = open(mutepath, "w+")
            for role in userroles:
                if str(role) != "@everyone":
                    usrole = str(role)
                    write = usrole + "\n"
                    f.write(write)
            f.close()
            await self.client.replace_roles(user, mutedrole)
            if time != 0:
                if time_type == "m":
                    embed = discord.Embed(
                    title = '',
                    description = '{} Has been muted for {} minute(s)'.format(user.mention, str(t_time)),
                    colour = discord.Colour.green()
                    )
                    await self.client.say(embed=embed)
                    await asyncio.sleep(time)
                    path = "servers/" + str(server.id) + "/muted/" + str(user.id) + ".txt"
                    with open(path) as fp:
                       line = fp.readline()
                       roles_to_give = []
                       while line:
                           role = discord.utils.get(server.roles, name=line.strip())
                           roles_to_give.append(role)
                           line = fp.readline()
                       fp.close()
                    await self.client.replace_roles(user, *roles_to_give)
                    embed = discord.Embed(
                    title = '',
                    description = '{} Has been unmuted.'.format(user.mention),
                    colour = discord.Colour.green()
                    )
                    await self.client.say(embed=embed)
                    os.remove(path)
                elif time_type == "h":
                    embed = discord.Embed(
                    title = '',
                    description = '{} Has been muted for {} hour(s)'.format(user.mention, str(t_time)),
                    colour = discord.Colour.green()
                    )
                    await self.client.say(embed=embed)
                    await asyncio.sleep(time)
                    path = "servers/" + str(server.id) + "/muted/" + str(user.id) + ".txt"
                    with open(path) as fp:
                       line = fp.readline()
                       roles_to_give = []
                       while line:
                           role = discord.utils.get(server.roles, name=line.strip())
                           roles_to_give.append(role)
                           line = fp.readline()
                       fp.close()
                    await self.client.replace_roles(user, *roles_to_give)
                    embed = discord.Embed(
                    title = '',
                    description = '{} Has been unmuted.'.format(user.mention),
                    colour = discord.Colour.green()
                    )
                    await self.client.say(embed=embed)
                    os.remove(path)

            else:
                embed = discord.Embed(
                title = '',
                description = '{} Has been muted.'.format(user.mention),
                colour = discord.Colour.green()
                )
                await self.client.say(embed=embed)
        else:
            embed = discord.Embed(
            title = '',
            description = 'You do not have permission to use this command.',
            colour = discord.Colour.red()
            )
            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def unmute(self, ctx, user: discord.Member):
        author = ctx.message.author
        server = author.server
        if self.is_mod_or_perms(server, author):
            with open('srv_settings.json', 'r') as f:
                servers = json.load(f)
                setting = servers[server.id]["Mute_Role"]
            mutedrole = discord.utils.get(server.roles, name=setting)
            if mutedrole == None:
                await self.client.say("There is no mute role yet, please use >muterole ROLE_NAME to set it.")
                return
            else:
                path = "servers/" + str(server.id) + "/muted/" + str(user.id) + ".txt"
                if os.path.exists(path):
                        path = "servers/" + str(server.id) + "/muted/" + str(user.id) + ".txt"
                        with open(path) as fp:
                           line = fp.readline()
                           roles_to_give = []
                           while line:
                               role = discord.utils.get(server.roles, name=line.strip())
                               roles_to_give.append(role)
                               line = fp.readline()
                           fp.close()
                        await self.client.replace_roles(user, *roles_to_give)
                        embed = discord.Embed(
                        title = '',
                        description = '{} Has been unmuted.'.format(user.mention),
                        colour = discord.Colour.green()
                        )
                        await self.client.say(embed=embed)
                        os.remove(path)
                else:
                    print("This user is not muted")
        else:
            embed = discord.Embed(
            title = '',
            description = 'You do not have permission to use this command.',
            colour = discord.Colour.red()
            )
            await self.client.say(embed=embed)
    @commands.command(pass_context=True)
    async def unmuteid(self, ctx, userID):
        author = ctx.message.author
        server = author.server
        user = server.get_member(userID)
        if self.is_mod_or_perms(server, author):
            with open('srv_settings.json', 'r') as f:
                servers = json.load(f)
                setting = servers[server.id]["Mute_Role"]
            mutedrole = discord.utils.get(server.roles, name=setting)
            if mutedrole == None:
                await self.client.say("There is no mute role yet, please use >muterole ROLE_NAME to set it.")
                return
            else:
                path = "servers/" + str(server.id) + "/muted/" + str(user.id) + ".txt"
                if os.path.exists(path):
                        path = "servers/" + str(server.id) + "/muted/" + str(user.id) + ".txt"
                        with open(path) as fp:
                           line = fp.readline()
                           roles_to_give = []
                           while line:
                               role = discord.utils.get(server.roles, name=line.strip())
                               roles_to_give.append(role)
                               line = fp.readline()
                           fp.close()
                        await self.client.replace_roles(user, *roles_to_give)
                        embed = discord.Embed(
                        title = '',
                        description = '{} Has been unmuted.'.format(user.mention),
                        colour = discord.Colour.green()
                        )
                        await self.client.say(embed=embed)
                        os.remove(path)
                else:
                    print("This user is not muted")
        else:
            embed = discord.Embed(
            title = '',
            description = 'You do not have permission to use this command.',
            colour = discord.Colour.red()
            )
            await self.client.say(embed=embed)

def setup(client):
    client.add_cog(Admin(client))

