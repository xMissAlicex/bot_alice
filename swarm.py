import discord
import asyncio
import time
import os
import json
import random
from discord.ext.commands import Bot
from discord.ext import commands
from random import randint

class Swarm:
    def __init__(self, client):
        self.client = client


    def update_brood(user, setting, set):
            with open('brood_list.json', 'r') as f:
                brood_list = json.load(f)
                brood_list[user.id][setting] = set
                with open('brood_list.json', 'w') as f:
                    json.dump(brood_list, f)

    @commands.command(pass_context=True)
    async def collect(self, ctx):
        author = ctx.message.author
        with open('brood_list.json') as json_file:
            brood_list = json.load(json_file)
            if not author.id in brood_list:
                await self.client.say("You do not have a brood, use >brood to create one.")
            else:
                collected = randint(53, 85)
                with open('brood_list.json', 'r') as f:
                    brood_list = json.load(f)
                    brood_list[author.id]["Organic_Material"] += collected
                    brood_list[author.id]['Hive_XP'] += 3
                    experience = brood_list[author.id]['Hive_XP']
                    lvl_start = brood_list[author.id]['Hive_Lvl']
                    lvl_end = int(experience ** (1/4))
                    if lvl_start < lvl_end:
                        brood_list[author.id]['Hive_Lvl'] = lvl_end
                        await self.client.say("You collected {} Organic Biomaterials and your Hive gained a level.".format(str(collected)))
                    else:
                        await self.client.say("You collected {} Organic Biomaterials".format(str(collected)))
                    with open('brood_list.json', 'w') as f:
                        json.dump(brood_list, f)



    @commands.command(pass_context=True)
    async def cleviathan(self, ctx, amount = 1):
        author = ctx.message.author
        with open('brood_list.json') as json_file:
            brood_list = json.load(json_file)
            if not author.id in brood_list:
                await self.client.say("You do not have a brood, use >brood to create one.")
            else:
                with open('brood_list.json', 'r') as f:
                    brood_list = json.load(f)
                    Material = brood_list[author.id]["Organic_Material"]
                    HiveLvL = brood_list[author.id]["Hive_Lvl"]
                if HiveLvL < 5:
                    await self.client.say("Your Hive needs to be at least Level 5 to create Leviathans")
                elif Material < 1000:
                    await self.client.say("You need at least 1.000 Organic Biomaterial for your drones to create a Leviathan Ship.")
                else:
                    print("Works")



    @commands.command(pass_context=True)
    async def spawneggs(self, ctx, amount = 1):
        author = ctx.message.author
        with open('brood_list.json') as json_file:
            brood_list = json.load(json_file)
            if not author.id in brood_list:
                await self.client.say("You do not have a brood, use >brood to create one.")
            else:
                with open('brood_list.json', 'r') as f:
                    brood_list = json.load(f)
                    InProgres = brood_list[author.id]["EggsInProgress"]
                    HiveLvL = brood_list[author.id]["Hive_Lvl"]
                    Allowed_Amount = int(HiveLvL)*3
                if InProgres == 1:
                    await self.client.say("You already have some eggs spawned, wait for them to hatch.")
                else:
                    if amount > Allowed_Amount:
                        await self.client.say("You are only allowed to spawn {} eggs since your Hive is level: {}.".format(str(Allowed_Amount), str(HiveLvL)))
                    else:
                        await self.client.say("You spawn {} eggs at your hive, wait 1 minute for them to hatch.".format(amount))
                        with open('brood_list.json', 'r') as f:
                            brood_list = json.load(f)
                            brood_list[author.id]["EggsInProgress"] = 1
                            with open('brood_list.json', 'w') as f:
                                json.dump(brood_list, f)
                        await asyncio.sleep(300)
                        spawned_zergs_amount = int(amount)*3
                        with open('brood_list.json', 'r') as f:
                            brood_list = json.load(f)
                            current_size = brood_list[author.id]["Brood_Size"]
                            brood_list[author.id]["EggsInProgress"] = 0
                            brood_list[author.id]["Brood_Size"] = current_size + spawned_zergs_amount
                            brood_list[author.id]['Hive_XP'] += 5
                            experience = brood_list[author.id]['Hive_XP']
                            lvl_start = brood_list[author.id]['Hive_Lvl']
                            lvl_end = int(experience ** (1/4))
                            if lvl_start < lvl_end:
                                brood_list[author.id]['Hive_Lvl'] = lvl_end
                                await self.client.say("{} Your spawned eggs hatch and out comes {} Zergs for your Swarm. Your Hive have also gained a level.".format(author.mention, str(spawned_zergs_amount)))
                            else:
                                await self.client.say("{} Your spawned eggs hatch and out comes {} Zergs for your Swarm.".format(author.mention, str(spawned_zergs_amount)))

                            with open('brood_list.json', 'w') as f:
                                json.dump(brood_list, f)


    @commands.command(pass_context=True)
    async def swarm(self, ctx):
        author = ctx.message.author
        server = ctx.message.server
        channel = ctx.message.channel
        with open('brood_list.json') as json_file:
            brood_list = json.load(json_file)
            if not author.id in brood_list:

                await self.client.say('You do not have a Swarm, do you wish to create one? (Yes/No)')
                user_response = await self.client.wait_for_message(timeout=30, channel=channel, author=author)
                if user_response.clean_content == 'yes' or user_response.clean_content == 'Yes':
                    await self.client.say("Brood Creation Initiated")
                    brood_list[author.id] = {}

                    await self.client.say('What do you want to name your swarm?')
                    user_response = await self.client.wait_for_message(timeout=30, channel=channel, author=author)
                    brood_list[author.id]['Brood_Name'] = user_response.clean_content

                    await self.client.say('What image would you like for your swarm(Full URL)')
                    user_response = await self.client.wait_for_message(timeout=30, channel=channel, author=author)
                    brood_list[author.id]['Brood_Image'] = user_response.clean_content

                    await self.client.say('What name would you like for your swarm leader?')
                    user_response = await self.client.wait_for_message(timeout=30, channel=channel, author=author)
                    brood_list[author.id]['Leader_Name'] = user_response.clean_content
                    brood_list[author.id]['Hive_Lvl'] = 1
                    brood_list[author.id]['Hive_XP'] = 0
                    brood_list[author.id]['Evolution_Stage'] = 1
                    brood_list[author.id]['Brood_Queens'] = 0
                    brood_list[author.id]['Swarm_Faction'] = "None"
                    brood_list[author.id]['Brood_Size'] = 10
                    brood_list[author.id]['Ultralisks'] = 0
                    brood_list[author.id]['Leviathans'] = 0
                    brood_list[author.id]['EggsInProgress'] = 0
                    brood_list[author.id]['Organic_Material'] = 100

                    await self.client.say('What is the name of your swarm home world?')
                    user_response = await self.client.wait_for_message(timeout=30, channel=channel, author=author)
                    brood_list[author.id]['Home_World'] = user_response.clean_content
                    brood_list[author.id]['Home_Infestion'] = 5
                    brood_list[author.id]['Planets_Infested'] = 1

                    with open('brood_list.json', 'w') as f:
                        json.dump(brood_list, f)
                        print("Brood has been created")
            else:
                with open('brood_list.json', 'r') as f:
                    brood_list = json.load(f)
                    broodname = brood_list[author.id]['Brood_Name']
                    broodimage = brood_list[author.id]['Brood_Image']
                    broodleader = brood_list[author.id]['Leader_Name']
                    broodqueens = brood_list[author.id]['Brood_Queens']
                    broodlvl = brood_list[author.id]['Hive_Lvl']
                    broodstage = brood_list[author.id]['Evolution_Stage']
                    broodfaction = brood_list[author.id]['Swarm_Faction']
                    broodsize = brood_list[author.id]['Brood_Size'] + brood_list[author.id]['Ultralisks'] + brood_list[author.id]['Ultralisks']
                    broodhome = brood_list[author.id]['Home_World']
                    broodhomeinfestation = brood_list[author.id]['Home_Infestion']
                    broodplanets = brood_list[author.id]['Planets_Infested']
                    broodlevis = brood_list[author.id]['Leviathans']
                    broodmat = brood_list[author.id]['Organic_Material']




                embed = discord.Embed(
                    title = '',
                    description = '',
                    colour = discord.Colour.blue()
                )
                embed.set_footer(text='For The Swarm!')
                embed.set_thumbnail(url=broodimage)
                embed.set_author(name='Swarm Information', icon_url='https://i.imgur.com/qT9B2iy.png')
                #embed.add_field(name='Swarm Type', value=broodname, inline=True
                embed.add_field(name='Swarm Name', value=broodname)
                embed.add_field(name='Swarm Leader', value=broodleader)
                embed.add_field(name='Swarm Stage', value=broodstage)
                embed.add_field(name='Swarm Homeworld', value=broodhome)
                embed.add_field(name='Swarm Home Infestation %', value=broodhomeinfestation)
                embed.add_field(name='Swarm Infested Planets', value=broodplanets)
                embed.add_field(name='Swarm Queens', value=broodqueens)
                embed.add_field(name='Swarm Size', value=broodsize)
                embed.add_field(name='Swarm Faction', value=broodfaction)
                embed.add_field(name='Swarm Leviathans', value=broodlevis)
                embed.add_field(name='Hive Level', value=broodlvl)
                embed.add_field(name='Organic Biomaterial', value=broodmat)
                await self.client.say(embed=embed)





def setup(client):
    client.add_cog(Swarm(client))
