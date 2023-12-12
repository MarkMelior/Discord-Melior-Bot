import asyncio
import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import CommandOnCooldown
import var
from function import deleteSlash, embed_func, deleteBtn
import config
from cooldowns import CallableOnCooldown



class Error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None


    @commands.Cog.listener()
    async def on_command_error( self, ctx, error ):
        #КОМАНДЫ НЕ СУЩЕСТВУЕТ
        if isinstance( error, commands.CommandNotFound ):
            emb = nextcord.Embed( description = f'❌ Команда не найдена. `{config.PREFIX}help`', color = config.cError )

        #НЕДОСТАТОЧНО ПРАВ
        elif isinstance( error, ( commands.MissingRole, commands.MissingAnyRole, commands.MissingPermissions ) ):
            emb = nextcord.Embed( description = f'❌ У вас недостаточно прав на выполнение данной команды. Отказано в доступе: `{ctx.command.aliases}`', color = config.cError )

        #КОМАНДА ВРЕМЕННО НЕДОСТУПНА
        elif isinstance( error, CallableOnCooldown ) or isinstance( error, CommandOnCooldown ):
            h = int(error.retry_after) // 3600  # часы
            m = (int(error.retry_after) - h * 3600) // 60  # мин
            s = int(error.retry_after) % 60  # секунды
            if h < 10:
                h = f"0{h}"
            if m < 10:
                m = f"0{m}"
            if s < 10:
                s = f"0{s}"
            time_reward = f"`{h}` часов `{m}` минут `{s}` секунд"

            emb = nextcord.Embed( description = f"❌ Команда `{ctx.command.aliases}` временно недоступна \n \n"+f'{time_reward}'.format( error.retry_after), color = config.cError )

        #ОШИБКА В КОМАНДЕ
        elif isinstance( error, (commands.UserInputError, commands.MissingRequiredArgument) ):
            emb = nextcord.Embed( description = f"❌ Ошибка в команде: `{ctx.command.aliases}`", color = config.cError )

        emb.set_footer(text='Это сообщение пропадёт автоматически')
        await ctx.reply( embed = emb, delete_after = 10 )
        await ctx.message.add_reaction("❌")
        def check( reaction, user ):
            return (user == ctx.message.author or user == ctx.guild.owner_id) and str( reaction.emoji ) == '❌'
        try:
            await self.bot.wait_for('reaction_add', timeout = 10, check = check )
        except asyncio.TimeoutError:
            await ctx.message.clear_reactions()
            return 
        else:
            await ctx.message.delete()

def setup(bot):
    bot.add_cog(Error(bot))
    print( 'Cogs - "Error" connected' )