import discord
from discord.ext import commands
from discord.ext.commands import cooldown
import random
import var



class Duel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.command( aliases = var.aDuel, brief = var.bDuel, usage = var.uDuel )
    @cooldown(1, 300, commands.BucketType.member)
    async def __duel(self, ctx, member: discord.Member = None):

        if member == ctx.author:
            await ctx.send(
                embed=discord.Embed(description=f':x: {ctx.message.author.mention} вы не можете вызвать себя на дуэль!',
                                    color=var.cError))
            return

        else:
            a = random.randint(1, 2)
            if a == 1:
                await ctx.send(embed=discord.Embed(
                    description=f":crossed_swords: {ctx.message.author.mention} выиграл(а) дуэль против {member.mention}",
                    color=var.cSuccess))
                await member.send(embed=discord.Embed(
                    description=f':crossed_swords: Вы потерпели поражение на дуэле против {ctx.message.author.mention}',
                    color=var.cError), delete_after=60)
                await ctx.message.author.send(
                    embed=discord.Embed(description=f':crossed_swords: Вы выиграли дуэль против {member.mention}',
                                        color=var.cSuccess), delete_after=60)

            else:
                await ctx.send(embed=discord.Embed(
                    description=f":crossed_swords: {ctx.message.author.mention} потерпел(а) поражение на дуэле против {member.mention}",
                    color=var.cError))
                await member.send(embed=discord.Embed(
                    description=f':crossed_swords: Вы выиграли дуэль против {ctx.message.author.mention}',
                    color=var.cError), delete_after=60)
                await ctx.message.author.send(embed=discord.Embed(
                    description=f':crossed_swords: Вы потерпели поражение на дуэле против {member.mention}',
                    color=var.cError), delete_after=60)


async def setup(bot):
    await bot.add_cog(Duel(bot))

print( 'Cogs - "Duel" connected' )
