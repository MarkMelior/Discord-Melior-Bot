import discord
from discord.ext import commands
import asyncio
import random
import var



class Roulette(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    # РУССКАЯ РУЛЕТКА КИК ИЗ ЧАТА
    @commands.command( aliases = var.aRoulette, brief = var.bRoulette, usage = var.uRoulette )
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_guild_permissions(manage_messages=True)
    async def russian_roulette( self, ctx ):
        try:
            channel = ctx.message.author.voice.channel
        except:
            return await ctx.send( ctx.author.name + ', почему ты играешь в рулетку на вылет, а сам не в голосовом чате?' )

        await ctx.message.delete()
        message = await ctx.send("``Через: 3``")
        await asyncio.sleep(0.5)
        await message.edit(content="``Через: 2``")
        await asyncio.sleep(0.5)
        await message.edit(content="``Через: 1``")
        await asyncio.sleep(0.5)
        dead = random.choice(channel.members)
        await message.edit(content=f"БУУМ")
        await asyncio.sleep(0.5)
        await dead.move_to(None)
        await message.edit(content=None, embed=discord.Embed(description=f'{dead.mention} словил пулю...'))





async def setup(bot):
    await bot.add_cog(Roulette(bot))

print( 'Cogs - "Roulette" connected' )