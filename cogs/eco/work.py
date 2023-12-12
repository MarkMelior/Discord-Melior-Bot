import nextcord
from nextcord.ext import commands
import var
import config
from nextcord.ext.commands import cooldown
from function import deleteSlash, embed_func, db_descBalance
from function import msgXp
from nextcord.utils import get
from nextcord import SlashOption
import cooldowns



class EcoWork(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

		
	# РАБОТА
	@nextcord.slash_command( description = var.bGameWork )
	@cooldowns.cooldown(1, config.delayWork, bucket = cooldowns.SlashBucket.author)
	async def work(self, ctx, *, work = SlashOption(
        name="work",
        choices={"🧩 Junior": "Junior", "💥 Middle": "Middle", "💎 Senior": "Senior"},
    )):
		
		if work == 'Senior' and (get(ctx.user.roles, id = config.rSenior) or get(ctx.user.roles, id = config.rBoosty)):
			salary = config.salarySenior
			xp = config.xpSenior
		elif work == 'Middle' and (get(ctx.user.roles, id = config.rMiddle) or get(ctx.user.roles, id = config.rBoosty)):
			salary = config.salaryMiddle
			xp = config.xpMiddle
		elif work == 'Junior':
			salary = config.salaryJunior
			xp = config.xpJunior
		else:
			work.reset_cooldown(ctx)
			await ctx.send('У вас нет нужных навыков в этой специальности \n \n `/shop` *- купить роль*')

		balance = db_descBalance(ctx.user.id, f"UPDATE users SET cash = cash + {salary}, xp = xp + {xp} WHERE id = {ctx.user.id}", True)
		emb = nextcord.Embed( description = f"{ctx.user.mention} заработал(а) **`{salary}$`** + **`{xp}xp`** \n \n :bar_chart: Профессия `{work}`" + balance, color = config.cSuccess )
		msg = await ctx.send( embed = emb )
		await deleteSlash(self, ctx, msg)
		await msgXp(ctx)

			

def setup(bot):
	bot.add_cog(EcoWork(bot))

print( 'Cogs - "EcoWork" connected' )