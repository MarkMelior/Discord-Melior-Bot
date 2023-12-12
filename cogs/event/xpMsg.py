import nextcord
from nextcord.ext import commands
import config
from SQL import cursor
import random


class xpMsg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    # ОПЫТ ЗА СООБЩЕНИЯ
    @commands.Cog.listener()
    async def on_message( self, msg ):
        from function import msgXp
        if len(msg.content) > 10 and msg.channel.id != config.kCasino:#за каждое сообщение длиной > 10 символов...
            cursor.execute(f'UPDATE users SET xp=xp+{random.randint(5, 20)} WHERE id={msg.author.id}')
            cursor.execute(f'UPDATE users SET msg=msg+1 WHERE id={msg.author.id}')
            await msgXp(msg.author)



def setup(bot):
    bot.add_cog(xpMsg(bot))

print( 'Cogs - "xpMsg" connected' )