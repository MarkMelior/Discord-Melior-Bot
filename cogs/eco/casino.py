import nextcord
from nextcord.ext import commands
import var
import config
from SQL import cursor
import random
from function import deleteSlash, db_balance_user, db_descBalance
from function import msgXp
from nextcord.utils import get


class EcoCasino(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

		
	#ИГРА В КАЗИНО
	# @nextcord.slash_command( description = var.bGameCasino )
	@commands.command( aliases = var.aGameCasino, brief = var.bGameCasino, usage = var.uGameCasino )
	async def __casino( self, ctx, amount ):

		# случайное число, на основе которого работает рандомизация
		number = random.randint(1, 1000)


		balance_user = db_balance_user(ctx.author.id)


		# КАЗИНО СТАВКА НА ВСЕ ДЕНЬГИ
		if amount in ['all', 'все', 'всё', 'вабанк', 'ва-банк']:
			amount = db_balance_user(ctx.author.id)

		amount = int(amount)

		# ОШИБКА: СУММА МЕНЬШЕ 1$
		if amount < 1:
			emb = nextcord.Embed( description = f"{ctx.author.mention} укажи сумму больше **1$** :leaves:!", color = config.cError )
			emb.set_footer(text=f'Ставка: {amount}$')
			msg = await ctx.send( embed = emb, delete_after = 10 )
			await deleteSlash(self, ctx, msg)
			return

		# ОШИБКА: НЕДОСТАТОЧНО СРЕДСТВ
		elif balance_user < amount:
			emb = nextcord.Embed( description = f'{ctx.author.mention} у вас недостаточно средств! \n \n :moneybag: Баланс: **{balance_user}$ :leaves:**', color = config.cError )
			emb.set_footer(text=f'Ставка: {amount}$')
			msg = await ctx.send( embed = emb, delete_after = 10 )
			await deleteSlash(self, ctx, msg)
			return

		else: # ЕСЛИ НЕТ ОШИБОК, ТО:
			lose = random.randint(1, 4)

			if number > 700: # ВЫИГРЫШ x2
				add = amount
				description = f'{ctx.author.mention} вы выиграли: **+{int(add)}$** :leaves: (x2) :slight_smile:',
				colorr = config.cSuccess
				cursor.execute(f'UPDATE users SET xp=xp+{random.randint(5, 20)} WHERE id={ctx.author.id}')
				await msgXp(ctx.author)
			elif number <= 30 and (get(ctx.author.roles, id = config.rx5Casino) or get(ctx.author.roles, id = config.rBoosty)): # ВЫИГРЫШ x5
				add = amount * 5
				description = f'{ctx.author.mention} вы выиграли: **+{int(add)}$** :leaves: (x5) :flushed:',
				colorr = config.cSuccess
				cursor.execute(f'UPDATE users SET xp=xp+{random.randint(20, 100)} WHERE id={ctx.author.id}')
				await msgXp(ctx.author)
			elif number <= 5 and (get(ctx.author.roles, id = config.rx5Casino) or get(ctx.author.roles, id = config.rBoosty)): # ВЫИГРЫШ x50
				add = amount * 50
				description = f'{ctx.author.mention} вы выиграли: **+{int(add)}$** :leaves: (x50) :money_mouth:',
				colorr = config.cWarn
				cursor.execute(f'UPDATE users SET xp=xp+{random.randint(100, 500)} WHERE id={ctx.author.id}')
				await msgXp(ctx.author)
			elif lose == 1: # ЕСЛИ ПРОИГРАЛ x0.75
				add = -(amount * 0.75)
				description = f'{ctx.author.mention} вы проиграли: **{int(add)}$** :leaves: (x0.25) :hushed:',
				colorr = config.cError
			elif lose == 2: # ЕСЛИ ПРОИГРАЛ x0.5
				add = -(amount * 0.5)
				description = f'{ctx.author.mention} вы проиграли: **{int(add)}$** :leaves: (x0.50) :pensive:',
				colorr = config.cError
			elif lose == 3: # ЕСЛИ ПРОИГРАЛ x0.25
				add = -(amount * 0.25)
				description = f'{ctx.author.mention} вы проиграли: **{int(add)}$** :leaves: (x0.75) :confused:',
				colorr = config.cError
			elif lose == 4: # ЕСЛИ ПРОИГРАЛ x0
				add = -amount
				description = f'{ctx.author.mention} вы проиграли: **{int(add)}$** :leaves: (x0) :x:',
				colorr = config.cError

			balance = db_descBalance(ctx.author.id, f"UPDATE users SET cash = cash + {add} WHERE id = {ctx.author.id}")
			emb = nextcord.Embed( description = description[0] + balance, color = colorr )
			emb.set_footer(text=f'Ставка: {amount}$')
			await ctx.send( embed = emb )






def setup(bot):
	bot.add_cog(EcoCasino(bot))
	print( 'Cogs - "EcoCasino" connected' )