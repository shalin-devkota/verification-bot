import discord
from discord.ext import commands,tasks
import sqlite3
import time

conn=sqlite3.connect('pending.db')
c=conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS pendinglist(userid TEXT,jointime INT)")
conn.commit()
c.close()
conn.close()



class Events(commands.Cog):
    def __init__(self,client):
        self.client=client

   
       


    @commands.Cog.listener()
    async def on_ready (self):
        await self.client.change_presence(status=discord.Status.online, activity=discord.Game("Fighting"))
        print("Bot is ready")
        

    
    @commands.Cog.listener()
    async def on_member_join(self,member):
        conn= sqlite3.connect('pending.db')
        c=conn.cursor()
        c.execute("INSERT INTO pendinglist(userid,jointime) VALUES (?,?)",(member.id,int(round(time.time()))))
        conn.commit()
        c.close()
        conn.close()
        print('Entry added')
        
    @commands.Cog.listener()
    async def on_member_remove(self,member):
        conn= sqlite3.connect('pending.db')
        c=conn.cursor()
        c.execute(f"DELETE FROM pendinglist WHERE userid='{member.id}'")
        conn.commit()
        c.close()
        conn.close()
   


def setup(client):
    client.add_cog(Events(client))

