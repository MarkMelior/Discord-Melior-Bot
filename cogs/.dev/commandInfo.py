import discord
from discord.ext import commands
import var


class commandInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ИНФОРМАЦИЯ О КОМАНДЕ
    @commands.command()
    async def infcomm(self, ctx, command):
        for i in self.bot.commands:
            if command == i.name:
                if i.aliases in ([], None, ''):
                    i.aliases = "Отсутствуют"
                else:
                    i.aliases = ", ".join(i.aliases)

                if i.description in ([], None, ''):
                    i.description = "Отсутствует"

                if i.usage in ([], None, ''):
                    i.usage = "Отсутствует"

                embed = discord.Embed(title=f"✍️ Команда gb.{command}", description=f"**⚙️ Использование:** {i.usage}",
                                      color=var.cMain)
                embed.add_field(name="📝 Описание:", value=i.description, inline=False)
                embed.add_field(name="🖇️ Другие названия:", value=i.aliases)
                await ctx.send(embed=embed)
                break


async def setup(bot):
    await bot.add_cog(commandInfo(bot))

print( 'Cogs - "commandInfo" connected' )