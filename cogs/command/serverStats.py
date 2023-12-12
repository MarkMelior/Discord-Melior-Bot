import nextcord
from nextcord.ext import commands
import config

class serverStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    # СТАТИСТИКА СЕРВЕРА
    @commands.command()
    async def stats(self, ctx):
        guild = ctx.guild
        guild_age = (ctx.message.created_at - guild.created_at).days
        created_at = f"{guild.created_at.strftime('%b %d %Y at %H:%M')}. Это {guild_age} дней назад!"
        totalmembers = ctx.guild.members
        channels = ctx.guild.channels
        textchannels = ctx.guild.text_channels
        voicechannels = ctx.guild.voice_channels
        roletotal = ctx.guild.roles

        embedserverinfo = nextcord.Embed(
        title=ctx.guild.name,color = config.cMain)
        embedserverinfo.set_thumbnail(url = ctx.guild.icon_url)
        embedserverinfo.add_field(name="Айди сервера:", value=guild.id, inline=True)
        embedserverinfo.add_field(name="Создатель сервера:", value=guild.owner.mention, inline=True)
        embedserverinfo.add_field(name="Создатель бота:", value=guild.owner.mention, inline=False)
        embedserverinfo.add_field(name="Количество участников:", value=f'{len(totalmembers)}', inline=False)
        embedserverinfo.add_field(name="В сети:", value=len({m.id for m in guild.members if m.status is not nextcord.Status.offline}))
        embedserverinfo.add_field(name="Каналы:", value=f'{len(channels)} [{len(textchannels)} Текстовых | {len(voicechannels)} Голосовых] ', inline=False)
        embedserverinfo.add_field(name="Количество ролей", value=f'{len(roletotal)}', inline=False)
        embedserverinfo.add_field(name="Регион сервера", value=guild.region, inline=False)
        embedserverinfo.add_field(name="Сервер был создан:", value=created_at, inline=False)
        embedserverinfo.set_footer(text=f"Серверный бот: {self.bot.user.name}")

        await ctx.send(embed = embedserverinfo)


def setup(bot):
    bot.add_cog(serverStats(bot))

print( 'Cogs - "serverStats" connected' )