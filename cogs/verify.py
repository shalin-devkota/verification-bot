import discord
from discord.ext import commands
import sqlite3

role_to_add_id = " "
role_to_remove_id = " "

class Verification(commands.Cog):
    def __init__(self,client):
        self.client=client

    @commands.command()
    async def verify(self,ctx,member:discord.Member):
        if ctx.message.author.guild_permissions.manage_roles:
            memberRoleIDs= getMemberRoleIDs(member)
            if 798389599407439902 in memberRoleIDs:
                
                roleToAdd = discord.utils.get(ctx.message.guild.roles,id=role_to_add_id)
                roleToRemove = discord.utils.get(ctx.message.guild.roles,id=role_to_remove_id)
                await member.remove_roles(roleToRemove)
                await member.add_roles(roleToAdd)
                embed=discord.Embed(colour=discord.Colour.green(),title=f"Verified {member.name}!",description=f"Verified by {ctx.message.author.mention}")
                embed.set_thumbnail(url=member.avatar_url)
                await ctx.send(embed=embed)
                removeFromPendingList(member)
            else:
                await ctx.send (embed=discord.Embed(colour=discord.Colour.red(), description="Member is already verified."))
        else:
            await ctx.send (embed=discord.Embed(colour=discord.Colour.red(), description="You don't have the permission to verify members."))  

    @verify.error
    async def verify_error(self,ctx,error):
        error = getattr(error, "original", error)
        if isinstance(error,commands.MissingRequiredArgument):
            embed=discord.Embed(colour=discord.Colour.red(), description="Please mention the name of the user to verify.")
            await ctx.send(embed=embed) 

                
             
def getMemberRoleIDs(member):
    roleIDs= []
    for role in member.roles:
        roleIDs.append(role.id)
    return roleIDs


def removeFromPendingList(member):
    conn= sqlite3.connect('pending.db')
    c=conn.cursor()
    c.execute(f"DELETE FROM pendinglist WHERE userid='{member.id}'")
    conn.commit()
    c.close()
    conn.close()
   



def setup(client):
    client.add_cog(Verification(client))
