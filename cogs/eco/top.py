import nextcord
from nextcord.ext import commands
import var
import config
from SQL import cursor
from function import deleteSlash
from nextcord import SlashOption


class EcoTop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    #ТОП ПОЛЬЗОВАТЕЛЕЙ
    @nextcord.slash_command( description = var.bGameTop )
    async def top(self, ctx, top = SlashOption(
        name="select",
        choices={"🍃 Топ по деньгам": 'cash', "✨ Топ по опыту": 'xp'},
    )):

        if top == 'cash':
            cursor.execute( 'SELECT id, cash FROM users ORDER BY cash DESC LIMIT 10' )
            symb = '$'
            emoji = ':leaves: Топ 10 по деньгам'
        elif top == 'xp':
            cursor.execute( 'SELECT id, xp FROM users ORDER BY xp DESC LIMIT 10' )
            symb = 'xp'
            emoji = ':sparkles: Топ 10 по опыту'

        embed = nextcord.Embed( title = f'{emoji}', color = config.cMain )
        counter = 0

        for row in cursor.fetchall():
            counter += 1
            embed.add_field( name = f'{ counter }. **`{ row[1] }{symb}`**', value = f'<@{row[0]}>', inline = False )

        msg = await ctx.send( embed = embed )
        await deleteSlash(self, ctx, msg)


def setup(bot):
	bot.add_cog(EcoTop(bot))

print( 'Cogs - "EcoTop" connected' )