import nextcord
from nextcord.ext import commands
import var
import config
from SQL import cursor
from function import deleteSlash


class EcoUser(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

		
	#СТАТИСТИКА ПОЛЬЗОВАТЕЛЯ
	# @commands.command( aliases = var.aGameStats, brief = var.bGameStats, usage = var.uGameStats )
	@nextcord.slash_command( description = var.bGameStats )
	async def user( self, ctx, member: nextcord.Member = None ):

		if not member:
			member = ctx.user

		cursor.execute(f"SELECT cash FROM users WHERE id = {member.id}")
		select_cash = cursor.fetchone()
		cursor.execute(f"SELECT xp FROM users WHERE id = {member.id}")
		select_xp = cursor.fetchone()
		cursor.execute(f"SELECT lvl FROM users WHERE id = {member.id}")
		select_lvl = cursor.fetchone()
		cursor.execute(f"SELECT msg FROM users WHERE id = {member.id}")
		select_msg = cursor.fetchone()
		cursor.execute(f"SELECT business_cash FROM users WHERE id = {member.id}")
		select_bus = cursor.fetchone()
		cursor.execute(f"SELECT crypto FROM users WHERE id = {member.id}")
		select_crypto = cursor.fetchone()

		embed = nextcord.Embed( description = f'**Статистика пользователя {member.mention}**', color = config.cMain )

		date_format = "%d.%m.%Y *(в %H:%M)*" 
		embed.add_field( name = ':gem: Уровень:', value = f'**`{select_lvl[0]} lvl`**', inline = True )
		embed.add_field( name = ':sparkles: Опыт:', value = f'**`{select_xp[0]}xp`**', inline = True )
		embed.add_field( name = ':leaves: Баланс:', value = f'**`{select_cash[0]}$`**', inline = True )
		embed.add_field( name = '💬 Кол-во сообщений:', value = f'**`{select_msg[0]}`**', inline = True )
		embed.add_field( name = '📊 Счёт бизнеса:', value = f'**`{select_bus[0]}$`**', inline = True )
		embed.add_field( name = '⚡️ Криптовалюта:', value = f'**`{select_crypto[0]} ✦`**', inline = True )
		embed.add_field( name = 'Присоединился к серверу', value = f'{member.joined_at.strftime(date_format)}', inline = False )
		embed.add_field( name = 'Зарегистрировался в дискорде', value = f'{member.created_at.strftime(date_format)}', inline = False )

		roles = member.roles
		role_list = ""
		for role in roles:
			role_list += f"<@&{ role.id }> "
		
		embed.add_field( name = 'Роли', value = role_list, inline = False )
		embed.set_author( name = ctx.user, icon_url = ctx.user.avatar )
		embed.set_thumbnail(url = member.avatar)

		msg = await ctx.send( embed = embed )
		await deleteSlash(self, ctx, msg)

def setup(bot):
	bot.add_cog(EcoUser(bot))

print( 'Cogs - "EcoUser" connected' )