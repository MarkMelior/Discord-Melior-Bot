import discord
from discord.ext import commands
import var




class SearchRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prev = []



    # СПИСОК ЛЮДЕЙ С РОЛЬЮ
    @commands.command()
    async def search( self, ctx, role: discord.Role ):
        generation = [member.mention for member in role.members]

        if len(generation) <= 0:
            emb = discord.Embed( title = f':x: Ошибка', color = role.color )
            emb.add_field(name=f'У пользователей нет данной роли:', value = f'<@&{role.id}>')
            emb.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
        else:
            emb = discord.Embed( color = role.color )
            emb.add_field(name=f'Поиск по роли: ', value = f'<@&{role.id}>', inline = False)
            emb.add_field(name=f'Пользователи имеющие указанную роль: ', value = f'**{", ".join(generation)}**', inline = False)
            emb.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
        try:
            return await ctx.send( embed = emb )
        except discord.HTTPException:
            return await ctx.send(embed = discord.Embed(title="❌ Ошибка!", description="Список людей получился слишком большой, отправка сообщения невозможна.", color= var.cError))




def setup(bot):
    bot.add_cog(SearchRole(bot))

print( 'Cogs - "SearchRole" connected' )