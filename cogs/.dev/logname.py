import discord
from discord.ext import commands
import var


class LogName(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prev = []



    @commands.Cog.listener()
    async def on_member_update( self, before, after ):
        if before.nick != after.nick:
            channel = self.bot.get_channel( var.kLog )
            emb = discord.Embed( description = f':recycle: **У пользователя {before.mention} был изменён ник.**', color = var.cMain)
            emb.add_field( name = '**Старый ник**', value = f'{before.nick}' )
            emb.add_field( name = '**Новый ник**', value = f'{after.nick}' )

            await channel.send( embed = emb )


def setup(bot):
    bot.add_cog(LogName(bot))

print( 'Cogs - "LogName" connected' )