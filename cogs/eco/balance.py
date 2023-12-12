import nextcord
from nextcord.ext import commands
import var
import config
from function import deleteSlash, db_balance_user


class EcoBalance(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	# БАЛАНС
	@nextcord.slash_command( description = var.bGameBalance )
	async def balance(self, ctx, member: nextcord.Member = None):
		if member is None:
			emb = nextcord.Embed( description = f'{ctx.user.mention} ваш баланс составляет: **{db_balance_user(ctx.user.id)}$ :leaves:**', color = config.cMain )
		else:
			emb = nextcord.Embed( description = f'Баланс пользователя {member.mention} составляет: **{db_balance_user(member.id)}$ :leaves:**', color = config.cMain )
		msg = await ctx.send( embed = emb )
		await deleteSlash(self, ctx, msg)


def setup(bot):
	bot.add_cog(EcoBalance(bot))

print( 'Cogs - "EcoBalance" connected' )