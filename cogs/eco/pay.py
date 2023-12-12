import nextcord
from nextcord.ext import commands
import var
import config
from SQL import connection, cursor
from function import db_balance_user


class EcoPay(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		

	#ПЕРЕВОД СРЕДСТВ ПОЛЬЗОВАТЕЛЮ
	# @commands.command( aliases = var.aGamePay, brief = var.bGamePay, usage = var.uGamePay )
	@nextcord.slash_command( description = var.bGamePay )
	async def pay(self, ctx, member: nextcord.Member, cash: int, *, text = None):

		#если меньше 1$:
		if cash < 1:
			await ctx.send(
				embed=nextcord.Embed(description=f":x: {ctx.user.mention} укажи сумму больше **1$** :leaves:!",
									color=config.cError))

		#если сумма больше ограничения:
		elif cash > config.limitTransfer:
			await ctx.send(embed=nextcord.Embed(
				description=f":x: {ctx.user.mention} вы не можете перевести сумму больше **1000000$** :leaves:!",
				color=config.cError))

		#если перевод самому себе
		elif member.id == ctx.user.id:
			await ctx.send(embed=nextcord.Embed(
				description=f":x: {ctx.user.mention} вы не межете перевести :leaves: самому себе!",
				color=config.cError))

		#если не хватает денег:
		elif db_balance_user(ctx.user.id) < cash: 
			await ctx.send(embed=nextcord.Embed(
				description=f':x: {ctx.user.mention} у вас недостаточно средств!',
				color=config.cError))

		else:
			cursor.execute(f"UPDATE users SET cash = cash - {cash} WHERE id = {ctx.user.id}")
			cursor.execute(f"UPDATE users SET cash = cash + {cash} WHERE id = {member.id}")
			connection.commit()


			if text is None:
				await ctx.send(embed=nextcord.Embed(
					description=f':money_with_wings: {ctx.user.mention} перевел(а) на счёт {member.mention}: **{cash}$** :leaves:',
					color=config.cSuccess))
				await member.send(embed=nextcord.Embed(
					description=f':money_with_wings: {ctx.user.mention} перевел(а) вам: **{cash}$** :leaves:',
					color=config.cSuccess))

			else:
				await ctx.send(embed=nextcord.Embed(
					description=f':money_with_wings: {ctx.user.mention} перевел(а) на счёт {member.mention}: **{cash}$** :leaves: со словами: ```{text}```',
					color=config.cSuccess))
				await member.send(embed=nextcord.Embed(
					description=f':money_with_wings: {ctx.user.mention} перевел(а) вам: **{cash}$** :leaves: со словами: ```{text}```',
					color=config.cSuccess))



def setup(bot):
	bot.add_cog(EcoPay(bot))
	print( 'Cogs - "EcoPay" connected' )