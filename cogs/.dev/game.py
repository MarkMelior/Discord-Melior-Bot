# КОМАНДЫ ИГРЫ:
# 1. Balance (user)
# 2. Bonus
# 3. Casino [amount]
# 4. Pay [member] [amount]
# 5. Work [work]




import discord
from discord.ext import commands

import var
from var import connection, cursor
from discord.ext.commands import BucketType
from discord.ext.commands import cooldown
import random
from Cybernator import Paginator
from function import embed_func, db_balance_user, db_xp_user, db_descBalance, deleteBtn
# import pymysql
from function import msgXp
from discord.utils import get


class Game(commands.Cog):
	def __init__(self, bot):
		self.bot = bot








# @client.command()
# @commands.has_permissions( administrator = True )
# async def banan(ctx, member: discord.Member, *, reason=None):
#     emb = discord.Embed(title=f':octagonal_sign: | Блокировка Пользователя __{member.name}__',description=f'\n:red_square: **Нажми на кнопку:**',color = var.cMain)
#     emb.set_thumbnail(url= member.avatar_url)
#     emb.set_footer(text=f'Вызвано: {ctx.author.name}', icon_url= ctx.author.avatar_url)
#     await ctx.send(
#         embed = emb,
#         components = [
#             Button(style=ButtonStyle.blue, label="Узнать информациб про бан"),
#         ]
#     )
#     res = await client.wait_for("button_click")
#     if res.channel == ctx.channel:
#         emb = discord.Embed(title=f':octagonal_sign: | Информация про бан __{member.name}__',description=f'\n:red_square: **Подробная информация про бан:**',color = var.cMain)
#         emb.set_footer(text=f'|  Вызвано Администратором: {ctx.author.name}', icon_url= ctx.author.avatar_url)
#         emb.set_thumbnail(url= member.avatar_url)
#         emb.add_field(name=':shield:  |  Имя Нарушителя:',value = member.name)
#         emb.add_field(name=' :drum:   |  Айди Нарушителя:',value = member.id)
#         emb.add_field(name=':ring:    |   Тег Нарушителя:',value = member.discriminator)
#         emb.add_field(name=':joystick:|    Причина Нарушения:',value = reason)
#         emb.add_field(name=':beginner:| Дата регестрации аккаунта:',value = ctx.author.created_at.strftime("%d.%m.%Y %H:%M:%S"))
#         emb.add_field(name=f':notebook:  | Дата присоедениния: ', value = f'{ctx.author.joined_at.strftime("%d.%m.%Y %H:%M:%S")}')
#         await res.respond(embed=emb)




# # УПРАВЛЕНИЕ COGS
# @client.command(  aliases = var.aCogsList, brief = var.bCogsList, usage = var.uCogsList  )
# @commands.is_owner()
# async def __cogslist( ctx ):
#     await ctx.send( embed = discord.Embed(description=f':white_check_mark: Список когов: {extensions}', color = var.cSuccess))

# @client.command( aliases = var.aLoad, brief = var.bLoad, usage = var.uLoad )
# @commands.is_owner()
# async def __load( ctx, extension ):
#     channel = client.get_channel( var.kLog )
#     client.load_extension(f"cogs.{extension}")
#     await channel.send( embed = discord.Embed(description=f':white_check_mark: **COG:** ``{extension}`` был подключен', color = var.cSuccess))

# @client.command( aliases = var.aUnload, brief = var.bUnload, usage = var.uUnload )
# @commands.is_owner()
# async def __unload( ctx, extension ):
#     channel = client.get_channel( var.kLog )
#     client.unload_extension(f"cogs.{extension}")
#     await channel.send( embed = discord.Embed(description=f':x: **COG:** ``{extension}`` был отключен', color = var.cError))
#     print( f'Cogs - "{extension}" disable' )





	# #ИГРА В КРАШ
	# @commands.command( aliases = var.aGameRoulette, brief = var.bGameRoulette, usage = var.uGameRoulette )
	# # @cooldown(1, 1, BucketType.user)
	# async def __crash( self, ctx, amount, bet ):
	# 	roulette = random.randint(0, 36)
	# 	red = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
	# 	black = [2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35]
	# 	red_text = ['red', 'красное', 'крас']
	# 	black_text = ['черное', 'чёрное', 'черн', 'чёрн', 'black']


	# 	balance_user = db_balance_user(ctx.author.id)
	# 	if amount < 1:
	# 		await ctx.send('Укажи сумму больше 1$')
	# 		return
	# 	elif balance_user < amount:
	# 		await ctx.send('Недостаточно средств!')
	# 		return

	# 	try:
	# 		if bet in (red_text + black_text):
	# 			pass
	# 		else:
	# 			await ctx.send('Ошибка')
	# 			return
	# 	except Exception as e:
	# 		print(e)

			
	# 	add = -int(amount)
	# 	wl = ['вы проиграли ставку', '']
	# 	if roulette == 0:
	# 		result = f'💚 Выпал {roulette}'
	# 		if bet in ['0', 'zero', 'null', 0]:
	# 			add = int(amount) * 10
	# 			wl = ['вы выиграли ставку', '+']
	# 	if roulette == bet:
	# 		add = int(amount) * 10
	# 		wl = ['вы выиграли ставку', '+']
	# 	if roulette in black:
	# 		result = f'🖤 Выпало черное - {roulette}'
	# 		if bet in black_text:
	# 			add = int(amount)
	# 			wl = ['вы выиграли ставку', '+']
	# 	if roulette in red:
	# 		result = f'❤️ Выпало красное - {roulette}'
	# 		if bet in red_text:
	# 			add = int(amount)
	# 			wl = ['вы выиграли ставку', '+']
		

	# 	balance = db_descBalance(ctx.author.id, f"UPDATE users SET cash = cash + {add} WHERE id = {ctx.author.id}")
		
	# 	embed = discord.Embed(description=f'{result} \n \n {ctx.author.mention} {wl[0]}: **{wl[1]}{add}$** :leaves:' + balance, color=var.cMain)
	# 	embed.set_footer(text=f'Ставка: {amount}$')
	# 	await ctx.send(embed = embed)






























	# # РУССКАЯ РУЛЕТКА КИК ИЗ ЧАТА
	# @commands.command( aliases = var.aRoulette, brief = var.bRoulette, usage = var.uRoulette )
	# @commands.cooldown(1, 5, commands.BucketType.user)
	# @commands.has_guild_permissions(manage_messages=True)
	# async def russian_roulette( self, ctx ):
	# 	import asyncio

	# 	try:
	# 		channel = ctx.message.author.voice.channel
	# 	except:
	# 		return await ctx.send( ctx.author.name + ', почему ты играешь в рулетку на вылет, а сам не в голосовом чате?' )
	# 	await ctx.message.delete()
	# 	message = await ctx.send("``Через: 3``")
	# 	await asyncio.sleep(0.5)
	# 	await message.edit(content="``Через: 2``")
	# 	await asyncio.sleep(0.5)
	# 	await message.edit(content="``Через: 1``")
	# 	await asyncio.sleep(0.5)
	# 	dead = random.choice(channel.members)
	# 	await message.edit(content=f"БУУМ")
	# 	await asyncio.sleep(0.5)
	# 	await dead.move_to(None)
	# 	await message.edit(content=None, embed=discord.Embed(description=f'{dead.mention} словил пулю...'))



	#TEST
	# @commands.command()	
	# async def test( self, ctx ):
	# 	await ctx.send( embed = discord.Embed( title = 'TEST', components = [ Button( style = ButtonStyle.green, label = 'Accept', emoji = '💸' ) ], color = var.cError ) )

		# response = await self.bot.wait_for('button_click')
		# if response.channel == ctx.channel:
		# 	if response.component.label == 'Accept':
		# 		await response.respond(content='Great!')
		# 	else:
		# 		await response.respond(content='ИДИ НАХУЙ')



async def setup(bot):
	await bot.add_cog(Game(bot))

print( 'Cogs - "Game" connected' )