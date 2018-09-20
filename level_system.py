import discord
import asyncio
import json
import pymysql
from discord.ext import commands

class Level_System:
    def __init__(self, client):
        self.client = client

    def create_user_database(self, user):
        conn = pymysql.connect(host='sql7.freesqldatabase.com', user='sql7257339', password='yakm4fsd4T', db='sql7257339')
        c = conn.cursor()
        sql = "INSERT INTO `user_levels` VALUES ({}, '1', '0')".format(str(user.id))
        c.execute(sql)
        conn.commit()
        conn.close()

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

    def add_experience(self, user, exp):
        conn = pymysql.connect(host='sql7.freesqldatabase.com', user='sql7257339', password='yakm4fsd4T', db='sql7257339')
        c = conn.cursor()
        sql = "SELECT exp from `user_levels` WHERE userid = {}".format(str(user.id))
        c.execute(sql)
        conn.commit()
        data = c.fetchone()
        conn.close()
        for row in data:
            current_exp = row
        new_exp = int(current_exp) + int(exp)
        conn = pymysql.connect(host='sql7.freesqldatabase.com', user='sql7257339', password='yakm4fsd4T', db='sql7257339')
        c = conn.cursor()
        sql = "UPDATE `user_levels` SET exp = %s where userid = %s"
        t = (new_exp, str(user.id))
        c.execute(sql, t)
        conn.commit()
        data = c.fetchone()
        conn.close()
        print("EXP added")

    def level_up(self, users, user, exp):
            experience = users[user.id]['experience']
            lvl_start = users[user.id]['level']
            lvl_end = int(experience ** (1/7))
            if lvl_start < lvl_end:
                users[user.id]['level'] = lvl_end
                return True
            else:
                return False


    async def on_message(self, message):
        channel = message.channel
        user = message.author
        server = channel.server
        if user.id != 485457192456290325:
            toggle = self.check_database(server, "Level_System")
            if toggle == True:
                conn = pymysql.connect(host='sql7.freesqldatabase.com', user='sql7257339', password='yakm4fsd4T', db='sql7257339')
                c = conn.cursor()
                sql = "SELECT 'level' from `user_levels` WHERE userid = {}".format(str(user.id))
                c.execute(sql)
                conn.commit()
                data = c.fetchone()
                conn.close()
                if data == None:
                    self.create_user_database(user)
                else:
                    self.add_experience(message.author, 5)
                    


    async def on_member_join(self, member):
        if member.id != 481468291928293376:
            with open('users.json', 'r') as f:
                users = json.load(f)
            self.update_data(users, member)

            with open('users.json', 'w') as f:
                json.dump(users, f)


def setup(client):
    client.add_cog(Level_System(client))
