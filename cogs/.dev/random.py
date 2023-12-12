import discord
from discord.ext import commands
import random
import var

from random import choice


class Random(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.command( aliases = var.aRandom, brief = var.bRandom, usage = var.uRandom )
    async def __random(self, ctx, number = None):
        await ctx.message.delete()

        answer = choice(['да', 'нет'])
        await ctx.send(answer)



async def setup(bot):
    await bot.add_cog(Random(bot))

print( 'Cogs - "Random" connected' )