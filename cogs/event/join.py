import nextcord
from nextcord.ext import commands
import var
import config
import random


class Join(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    # СООБЩЕНИЕ ПОЛЬЗОВАТЕЛЮ, КОТОРЫЙ ПРИСОЕДИНИЛСЯ
    @commands.Cog.listener()
    async def on_member_join( self, member ):
        channel = self.bot.get_channel( config.kStart )

        name = [ 'Добро пожаловать', 'Встречайте' ]
        conn = [ 'уже с нами!', 'уже здесь', 'проскальзывает на сервер', 'присоединяется к нашей тусовке',
                 'приземляется на сервер', 'запрыгивает на сервер', 'залетает с ноги' ]
        gift = [ 'печеньку 🍪', 'конфетку 🍬', 'шоколадку 🍫', 'чупик 🍭', 'арбуз 🍉', 'клубничку 🍓', 'морожко 🍦', 'виноград 🍇', 'яблоко 🍎' ]
        emoji = [ '🥳', '🤩', '🎆', '🎉' ]

        random_name = random.randint(0, len(name) - 1)
        random_conn = random.randint(0, len(conn) - 1)
        random_gift = random.randint(0, len(gift) - 1)
        random_emoji = random.randint(0, len(emoji) - 1)

        #ПРИВЕТСТВИЕ В ЛС ПОЛЬЗОВАТЕЛЯ
        emb = nextcord.Embed(title=f'🥰 {member.name}, привет!', description = f'Хочешь узнать, что умеет бот? \n Напиши `{config.PREFIX}{var.aHelp[0]}` в чате на сервере', color = config.cMain)
        emb.set_footer(text=f"Держи от меня {gift[random_gift]}")
        emb.set_thumbnail( url = 'https://i.ibb.co/L9ST4Hz/image.png' )
        await member.send( embed = emb )

        # ПРИВЕТСТВИЕ В ЧАТЕ
        embed = nextcord.Embed( title = f"{emoji[random_emoji]} {name[random_name]}!", description = f'{member.mention} {conn[random_conn]}', color = config.cMain )
        await channel.send( embed = embed )



    # СООБЩЕНИЕ ПОЛЬЗОВАТЕЛЮ, КОТОРЫЙ ПОКИНУЛ КАНАЛ
    @commands.Cog.listener()
    async def on_member_remove( self, member ):
        channel = self.bot.get_channel( config.kStart )
        await channel.send( embed = nextcord.Embed( description = f'{member.mention} покинул сервер', color = config.cError ) )









def setup(bot):
    bot.add_cog(Join(bot))

print( 'Cogs - "Join" connected' )