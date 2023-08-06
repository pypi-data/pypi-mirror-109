import discord
from discord.ext import commands

async def ban(ctx, user: discord.User, reason=None):
    if reason is None:
        reason = Default

    else:
        embed = discord.Embed(title=f"{user.display_name}#{user.discriminator} has been banned", color=discord.Color.red())
        await ctx.send(embed=embed)
        await ctx.guild.ban(user=user)