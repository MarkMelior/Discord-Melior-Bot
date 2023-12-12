import nextcord
from nextcord.ext import commands
import config
import random



class blockPrivateMsg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    #БЛОКИРОВКА ЛИЧНЫХ СООБЩЕНИЙ & ЧАТ БОТ
    @commands.Cog.listener()
    async def on_message( self, msg ):
        if msg.author.id != self.bot.user.id:
            if msg.guild:
                await self.bot.process_commands( msg )
            else:
                a = random.choice([ 'Я не общаюсь в личных сообщениях. Сорри :<', 'Прости, не отвечаю в ЛС', 'Хватит мне писать в личку' ])
                await msg.author.send( a )
                # channel = self.bot.get_channel( config.kBotMessage )
                # emb = nextcord.Embed(description = f':incoming_envelope: **{msg.author.mention}** отправил боту: ```{msg.content}```', color = config.cMain )
                # await channel.send( embed = emb )
                return



def setup(bot):
    bot.add_cog(blockPrivateMsg(bot))

print( 'Cogs - "blockPrivateMsg" connected' )