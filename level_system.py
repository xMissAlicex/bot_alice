import discord
import asyncio
import json
from discord.ext import commands

class Level_System:
    def __init__(self, client):
        self.client = client

    def add_experience(self, users, user, exp):
        users[user.id]['experience'] += exp

    def level_up(self, users, user, exp):
            experience = users[user.id]['experience']
            lvl_start = users[user.id]['level']
            lvl_end = int(experience ** (1/7))
            if lvl_start < lvl_end:
                users[user.id]['level'] = lvl_end
                return True
            else:
                return False

    def update_data(self, users, user):
            if not user.id in users:
                users[user.id] = {}
                users[user.id]['experience'] = 0
                users[user.id]['level'] = 1

    async def on_message(self, message):
        channel = message.channel
        user = message.author
        server = channel.server
        with open('srv_settings.json', 'r') as f:
            servers = json.load(f)
            toggle = servers[server.id]["Level_System"]
        if toggle == True:
            if user.id != 481468291928293376:
                with open('users.json', 'r') as f:
                    users = json.load(f)

                self.update_data(users, message.author)
                self.add_experience(users, message.author, 5)
                if self.level_up(users, message.author, message.channel):
                    await self.client.send_message(channel, "{} You have gained a level!".format(user.mention))
                with open('users.json', 'w') as f:
                    json.dump(users, f)


    async def on_member_join(self, member):
        if member.id != 481468291928293376:
            with open('users.json', 'r') as f:
                users = json.load(f)

            await self.update_data(users, member)

            with open('users.json', 'w') as f:
                json.dump(users, f)


def setup(client):
    client.add_cog(Level_System(client))
