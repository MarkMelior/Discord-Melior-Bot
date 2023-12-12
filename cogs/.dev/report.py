import discord
from discord.ext import commands
from discord.ext.commands import cooldown
import var


class Report(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command( aliases = var.aReport, brief = var.bReport, usage = var.uReport )
    @cooldown( 1, 86400, commands.BucketType.member )
    async def __report( self, ctx, *, text ):
        await ctx.channel.purge( limit = 1 )

        channel = self.bot.get_channel( var.kModer )

        embed1 = discord.Embed( title = ':white_check_mark: Ваше сообщение на рассмотрении!',
                              description = f'```Текст: {text}```', color = var.cSuccess )
        await ctx.author.send( embed = embed1)


        emb = discord.Embed(
            description = f':white_check_mark: **{ctx.message.author.mention}** отправил сообщение модерации: ```Текст: {text}```',
            color = var.cSuccess )
        await channel.send( embed = emb )



def setup(bot):
    bot.add_cog(Report(bot))

print( 'Cogs - "Report" connected' )