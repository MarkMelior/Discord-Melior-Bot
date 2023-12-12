import discord
from discord.ext import commands
import var



class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    async def status_func( self, ctx, desc, arg ):
        channel = self.bot.get_channel(var.kLog)
        embed = discord.Embed( title = 'Статус бота изменен!', color = var.cMain, description = desc + arg )
        await self.bot.change_presence( status = discord.Status.online, activity = discord.Game( name = arg ) )
        await channel.send( embed = embed )
        await ctx.message.delete()
        return


    # .plays
    @commands.command( aliases = var.aStatusPlaying )
    @commands.has_any_role( var.pStatus )
    async def __status_playing( self, ctx, *, arg ):
        await status_func( self, ctx, 'Бот теперь играет в ', arg )


    # .watch
    @commands.command( aliases = var.aStatusWatch )
    @commands.has_any_role( var.pStatus )
    async def __status_watch( self, ctx, *, arg ):
        await status_func( self, ctx, 'Бот теперь смотрит ', arg )
        
        # channel = self.bot.get_channel(var.kLog)
        # embed = discord.Embed( title = 'Статус бота изменен!', color = var.cMain, description = 'Бот теперь смотрит ' + arg )
        # await self.bot.change_presence( status = discord.Status.online, activity = discord.Activity( name = arg, type = discord.ActivityType.watching ) )
        # await channel.send( embed = embed )
        # await ctx.message.delete()

    # .listen
    @commands.command( aliases = var.aStatusListen )
    @commands.has_any_role( var.pStatus )
    async def __status_listen( self, ctx, *, arg ):
        await status_func( self, ctx, 'Бот теперь слушает ', arg )

        # channel = self.bot.get_channel(var.kLog)
        # embed = discord.Embed( title = 'Статус бота изменен!', color = var.cMain, description = 'Бот теперь слушает ' + arg )
        # await self.bot.change_presence( status = discord.Status.online, activity = discord.Activity( name = arg, type = discord.ActivityType.listening ) )
        # await channel.send( embed = embed )
        # await ctx.message.delete()

    # .stream
    @commands.command( aliases = var.aStatusStream )
    @commands.has_any_role( var.pStatus )
    async def __status_stream( self, ctx, *, arg ):
        await status_func( self, ctx, 'Бот теперь стримит ', arg )

        # channel = self.bot.get_channel(var.kLog)
        # embed = discord.Embed( title = 'Статус бота изменен!', color = var.cMain, description = 'Бот теперь стримит ' + arg )
        # await self.bot.change_presence( status = discord.Status.online, activity = discord.Streaming( name = arg , url = 'url' ) )
        # await channel.send( embed = embed )
        # await ctx.message.delete()



async def setup(bot):
    await bot.add_cog(Status(bot))

print( 'Cogs - "Status" connected' )