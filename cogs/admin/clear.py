import nextcord
from nextcord.ext import commands
from nextcord.ext import application_checks
import config
from function import deleteSlash


class AdminClear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ОЧИСТКА ЧАТА
    @nextcord.slash_command( description = 'Очистить чат' )
    @application_checks.is_owner()
    async def clear( self, ctx, amount: int ):
        await ctx.channel.purge(limit = amount + 1)
        msg = await ctx.send( embed = nextcord.Embed( description = f':white_check_mark: Удалено `{ amount }` сообщений', colour = config.cSuccess ) )
        await deleteSlash(self, ctx, msg)

def setup(bot):
    bot.add_cog(AdminClear(bot))

print( 'Cogs - "AdminClear" connected' )