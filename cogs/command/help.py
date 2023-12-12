import nextcord
from nextcord.ext import commands
from Cybernator import Paginator
import var
import config
from function import deleteSlash, setAuthor
from nextcord import SlashOption
from nextcord.ext.commands import BucketType
from nextcord.ext.commands import cooldown

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @nextcord.slash_command( description = 'Посмотреть все доступные команды' )
    @cooldown(1, 10, BucketType.user)
    async def help( self, ctx ):
        emb = nextcord.Embed( title = f'Помощь', description='''
        Все команды вы можете использовать введя `/` в текстовое поле
        
        **Как получить доступ к другим каналам?**
        - Купить необходимую роль в `/shop`
        Возможности всех ролей: <#1094883300180512808>

        **Как получать опыт?**
        Проявляйте активность на сервере. Опыт даётся за:
        - Сообщения
        - Выигрыш в казино
        - Работу
        - Бонус
        *В скором времени опыт будет начисляться за кол-во проведённого времени в голосовом канале*
        
        **Что делает реакция корзины под сообщением?**
        - Нажав на неё, вы удалите своё сообщение и сообщение отправленное ботом

        Остальные команды, которых нет в **Slash commands**:
        ''', color = config.cMain )
        emb.add_field(name=f'{var.uGameCasino}', value=f'{var.bGameCasino}', inline=False)
        if ctx.user.id == ctx.guild.owner_id:
            emb.add_field( name = f'{var.uClear}', value = f'{var.bClear}', inline = False )
            emb.add_field( name = f'{var.uAllSend}', value = f'{var.bAllSend}', inline = False )
            emb.add_field( name = f'{var.uUserSend}', value = f'{var.bUserSend}', inline = False )
            emb.add_field( name = f'{var.uCogsList}', value = f'{var.bCogsList}', inline = False )
            emb.add_field( name = f'{var.uLoad}', value = f'{var.bLoad}', inline = False )
            emb.add_field( name = f'{var.uUnload}', value = f'{var.bUnload}', inline = False )
            emb.add_field( name = f'{var.uRoleSend}', value = f'{var.bRoleSend}', inline = False )

        msg = await ctx.send( embed = emb )
        await deleteSlash(self, ctx, msg)


def setup(bot):
    bot.add_cog(Help(bot))

print( 'Cogs - "Help" connected' )