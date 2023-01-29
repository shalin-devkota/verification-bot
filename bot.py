import discord 
from discord.ext import commands, tasks
from discord.utils import get
import os
import sqlite3
import time


client = commands.Bot(command_prefix="=",case_insensitive=True)
client.remove_command("help")



#loads all the cogs inside the cogs folder on startup
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')    


@client.command()
#to load a cog
async def load(ctx,cname):
    author=ctx.message.author.id #gets the author's id.
    if author==397648789793669121: #checks if the authors id matches the owner's id.
        client.load_extension(f"cogs.{cname}")
        await ctx.send(f"Successfully loaded {cname}")
    else:
        await ctx.send("Only the bot owner can use this command.")

@client.command()
# to unload a cog
async def unload(ctx,cname):
    author=ctx.message.author.id #gets the author's id.
    if author==397648789793669121: #checks if the authors id matches the owner's id.
        client.unload_extension(f"cogs.{cname}")
    else:
        await ctx.send("Only the bot owner can use this command!")
    
@client.command()
#to reaload an ALREADY LOADED cog
async def reload(ctx,cname):
    author=ctx.message.author.id #gest the author's id.
    if author==397648789793669121: #checks if the authors id matches the owner's id.
        client.unload_extension(f"cogs.{cname}")
        client.load_extension(f"cogs.{cname}")
        await ctx.send(f"Successfully reloaded {cname}.")
    else:
        await ctx.send("Only the bot owner can use this command!")



@tasks.loop(seconds=3600)
async def dbclear():
    guild = client.get_guild(769728227991355494)
    conn = sqlite3.connect('pending.db')
    c=conn.cursor()
    c.execute("SELECT * FROM pendinglist")
    pendingUsers =c.fetchall()
    
    for user in pendingUsers:
        userJoinTime = user[1]
        currentTime= int(round(time.time()))
        userID = int(user[0])
        user = guild.get_member(userID)
        if user is not None:
            if currentTime - userJoinTime >= 86400:
                print (currentTime-userJoinTime)
                await user.kick(reason="Too late")
                print('Kicked!')
        
    print ('Iteration over')
        

@client.event
async def on_ready():
    dbclear.start()


client.run('TOKEN HERE ')



 

