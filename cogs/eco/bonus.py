import nextcord
from nextcord.ext import commands
import var
# from nextcord.ext.commands import BucketType
# from nextcord.ext.commands import cooldown
import cooldowns
from cooldowns import CooldownBucket
from cooldowns import CallableOnCooldown
import random
from function import deleteSlash, db_descBalance
from function import msgXp
from nextcord.utils import get
import config


class EcoBonus(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

		
	# БОНУС: ДЕНЬГИ + ОПЫТ
	@nextcord.slash_command( description = var.bGameBonus )
	@cooldowns.cooldown(1, 7200, bucket = cooldowns.SlashBucket.author)
	async def bonus( self, ctx ):
		bonn = random.randint(1, 10) # шанс получения бонуса

		if get(ctx.user.roles, id = config.rBoosty) or get(ctx.user.roles, id = config.r2xBonus):
			bonus_cash = config.cashBonus * 2
			bonus_xp = config.expBonus * 2
			bonn = 5
		else:
			bonus_cash = config.cashBonus
			bonus_xp = config.expBonus

		if bonn > 1: # шанс получить бонус 90%
			emb = nextcord.Embed( description = f'''{ctx.user.mention} получил бонус: **`{bonus_cash}$`** + **`{bonus_xp}xp`**''' + db_descBalance(ctx.user.id, f"UPDATE users SET cash = cash + {bonus_cash}, xp = xp + {bonus_xp} WHERE id = {ctx.user.id}", True), color = config.cSuccess )
			emb.set_footer(text=f'Следуший бонус можно получить через: {7200 / 60 / 60} часа')
			msg = await ctx.send( embed = emb )
			await deleteSlash(self, ctx, msg)
			await msgXp(ctx.user)
		else:
			emb = nextcord.Embed( description = f"{ctx.user.mention} тебе не дали бонус. Приходи в следующий раз", color = config.cError )
			emb.set_footer(text=f'Следуший бонус можно получить через: {7200 / 60 / 60} часа')
			msg = await ctx.send( embed = emb )
			await deleteSlash(self, ctx, msg)
    
	@bonus.error
	async def bonus_error(self, ctx, error):
		if isinstance( error, CallableOnCooldown ):
			await ctx.send(f"This command is on cooldown. Please try again in {error.retry_after:.2f} seconds.")
		else:
			raise error


def setup(bot):
	bot.add_cog(EcoBonus(bot))
	print( 'Cogs - "EcoBonus" connected' )