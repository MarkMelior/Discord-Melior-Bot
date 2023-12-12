# КОМАНДЫ МОДЕРАЦИИ:
# 1. Clear (amount)
# 2. Ban [member] [time (минуты)] 
# 3. Warn [member] [text]
# 4. Allsend [text]
# 5. Usersend [member] [text]
# 6. Rolesend [member] [text]




import discord
from discord.ext import commands
import asyncio
import var
from var import cursor, connection
from function import embed_func



class Moder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    # todo ОЧИСТКА ЧАТА
    @commands.command( aliases = var.aClear, brief = var.bClear, usage = var.uClear  )
    @commands.has_any_role( var.pClear )
    async def __clear( self, ctx, amount = 1 ):
        await ctx.channel.purge( limit = amount + 1 )
        await ctx.send( embed = discord.Embed( description = f':white_check_mark: Удалено { amount } сообщений', colour = var.cSuccess ), delete_after = var.dClear )


    # # ВРЕМЕННАЯ БЛОКИРОВКА
    # @commands.command( aliases = var.aBan, brief = var.bBan, usage = var.uBan )
    # @commands.has_any_role( var.pBan )
    # async def __ban(self, ctx, member: discord.Member = None, time=int(), *, reason):


    #     # ? FUNCTION: EMBED
    #     try:
    #         async def embed_ban(descText, btnDel = None, autoDel = None, sendMember = None, sendChannel = None, self = self, ctx = ctx, member = member):
    #             await embed_func(
    #                 desc = descText, #ОСНОВНАЯ ИНФОРМАЦИЯ
    #                 col = var.cError, # ЦВЕТ EMBED
    #                 # title = None, # ЗАГОЛОВОК
    #                 authorMsg = True, # ОТОБРАЗИТЬ АВТОРА, КОТОРЫЙ ВЫЗВАЛ КОМАНДУ
    #                 # field_name = None, field_value = None, # ИМЯ И ЗНАЧЕНИЕ
    #                 # img_url = None, # КАРТИНКА
    #                 # footer_text = None, # FOOTER ТЕКСТ

    #                 deleteMsg = True, # УДАЛИТЬ СООБЩЕНИЕ АВТОРА
    #                 deleteBtn = btnDel, # УДАЛЕНИЕ СООБЩЕНИЯ НАЖАВ НА РЕАКЦИЮ
    #                 deleteAuto = autoDel, # АВТОМАТИЧЕСКОЕ УДАЛЕНИЕ ЧЕРЕЗ [время в секундах]

    #                 # reactionMsg = None, # ДОБАВИТЬ РЕАКЦИЮ НА СООБЩЕНИЕ АВТОРА [true=✅, false=❌]

    #                 channelSend = sendChannel, # ОТПРАВИТЬ СООБЩЕНИЕ В КАНАЛ [id канала]
    #                 MemberSend = sendMember, # ОТПРАВИТЬ СООБЩЕНИЕ В ЛС [текст сообщения]
    #                 # MemberDelete = None, # УДАЛИТЬ ЧЕРЕЗ [время в секундах]

    #                 self = self, ctx = ctx, member = member # ТЕХНИЧЕСКИЕ КОММАНДЫ
    #                 )
    #     except Exception as e:
    #         print(f"error EMBED GIFT: {e}")



    #     if member == ctx.author:
    #         await embed_ban(
    #             descText = f':x: {ctx.message.author.mention} вы не можете заблокировать себя',
    #             btnDel = True,
    #             autoDel = 10,
    #             sendMember = None
    #             )
    #         return

    #     elif member.id == ctx.guild.owner.id:
    #         await embed_ban(
    #             descText = f':x: {ctx.message.author.mention} вы не можете заблокировать создателя сервера!',
    #             btnDel = True,
    #             autoDel = 10,
    #             sendMember = None
    #             )
    #         return

    #     elif ctx.author.top_role.position < member.top_role.position:
    #         await embed_ban(
    #             descText = f':x: {ctx.message.author.mention} вы не можете заблокировать участника, у которого роль выше чем ваша!',
    #             btnDel = True,
    #             autoDel = 10,
    #             sendMember = None
    #             )
    #         return

    #     else:
    #         cursor.execute(f"UPDATE users SET ban = ban + {1} WHERE id = {member.id}")
    #         cursor.execute(f"UPDATE users SET banned = {1} WHERE id = {member.id}")
    #         connection.commit()

    #         await member.add_roles(discord.utils.get(ctx.message.guild.roles, id = var.rBan))

    #         await embed_ban(
    #             descText = f'Пользователь {member.mention} был временно заблокирован за нарушение прав {ctx.message.author.mention} ```Длительность: {time} минут(ы)``` ```Причина: {reason}```',
    #             btnDel = False,
    #             autoDel = None,
    #             sendMember = f'Вы были временно заблокированы на **{var.NAME}** {ctx.message.author.mention} ```Длительность: {time} минут(ы)``` ```Причина: {reason}```',
    #             sendChannel = var.kModer
    #             )


    #         await asyncio.sleep(time * 60) # ДЛИТЕЛЬНОСТЬ
            
    #         cursor.execute(f"UPDATE users SET banned = {1} WHERE id = {member.id}")
    #         connection.commit()
    #         await member.remove_roles(discord.utils.get(ctx.message.guild.roles, id = var.rBan))

    #         await embed_ban(
    #             descText = f'Пользователь {member.mention} был временно заблокирован за нарушение прав {ctx.message.author.mention} ```Длительность: {time} минут(ы)``` ```Причина: {reason}```',
    #             btnDel = False,
    #             autoDel = None,
    #             sendMember = f'Вы были временно заблокированы на **{var.NAME}** {ctx.message.author.mention} ```Длительность: {time} минут(ы)``` ```Причина: {reason}```',
    #             sendChannel = var.kModer
    #             )

    #         await embed_func(
    #             self = self, ctx = ctx, member = member,

    #             desc = f':white_check_mark: Пользователь {member.mention} разбанен по истечению времени ```Длительность: {time} минут(ы)```', #ОСНОВНАЯ ИНФОРМАЦИЯ
    #             col = var.cSuccess, # ЦВЕТ EMBED
    #             # title = 'TITLE', # ЗАГОЛОВОК
    #             authorMsg = True, # ОТОБРАЗИТЬ АВТОРА, КОТОРЫЙ ВЫЗВАЛ КОМАНДУ
    #             # field_name = 'FIELD NAME', field_value = 'FIELD VALUE', # ИМЯ И ЗНАЧЕНИЕ
    #             # img_url = '', # КАРТИНКА
    #             # footer_text = 'FOOTER TEXT', # FOOTER ТЕКСТ

    #             MemberSend = f':white_check_mark: Вы были разбанены по истечению времени на **{var.NAME}** ```Длительность: {time} минут(ы)```', # ОТПРАВИТЬ СООБЩЕНИЕ В ЛС [текст сообщения]
    #             MemberDelete = None, # УДАЛИТЬ ЧЕРЕЗ [время в секундах]

    #             channelSend = var.kModer # ОТПРАВИТЬ В КАНАЛ [id канала]
    #             )


    # # todo ПРЕДУПРЕЖДЕНИЕ
    # @commands.command( aliases = var.aWarn, brief = var.bWarn, usage = var.uWarn )
    # @commands.has_any_role( var.pWarn )
    # async def __warn(self, ctx, member: discord.Member = None, *, reason):

    #     if member == ctx.author:
    #         await ctx.send(
    #             embed=discord.Embed(description=f':x: {ctx.message.author.mention} вы не можете предупредить себя',
    #                                 color=var.cError), delete_after=var.dError)
    #         return

    #     elif member.id == ctx.guild.owner.id:
    #         await ctx.send(embed=discord.Embed(
    #             description=f':x: {ctx.message.author.mention} вы не можете предупреждать создателя сервера!',
    #             color=var.cError), delete_after=var.dError)
    #         return

    #     else:
    #         cursor.execute(f"UPDATE users SET warn = warn + {1} WHERE id = {member.id}")
    #         connection.commit()

    #         await ctx.send(embed=discord.Embed(
    #             description=f'Пользователь {member.mention} был предупреждён {ctx.message.author.mention} ```Причина: {reason}```',
    #             color=var.cWarn))
    #         await member.send(embed=discord.Embed(
    #             description=f'Вы были предупреждены на **{var.NAME}** {ctx.message.author.mention} ```Причина: {reason}```',
    #             color=var.cWarn))


    # # todo ОТПРАВИТЬ СООБЩЕНИЕ ВСЕМ [от имени бота]
    # @commands.command( aliases = var.aAllSend, brief = var.bAllSend, usage = var.uAllSend )
    # @commands.has_permissions( administrator = True )
    # async def __allsend( self, ctx, *, message ):
    #     # await ctx.message.delete()
    #     members = ctx.guild.members
    #     for member in members:
    #         try:
    #             await member.send( message )
    #         except:
    #             print("Не могу отправить: '" + message + "'" + member.name)
    #     channel = self.bot.get_channel(var.kBotMessage)
    #     emb = discord.Embed(description=f':incoming_envelope: **{ctx.author.mention}** отправил всем: ```{message}```', color=var.cSuccess)
    #     await channel.send(embed=emb)


    # # todo ОТПРАВИТЬ СООБЩЕНИЕ ПОЛЬЗОВАТЕЛЯМ [от имени бота]
    # @commands.command( aliases = var.aUserSend, brief = var.bUserSend, usage = var.uUserSend )
    # @commands.has_permissions( administrator = True )
    # async def __usersend( self, ctx, member: discord.Member, *, message ):
    #     # await ctx.message.delete()
    #     await member.send( message )
    #     print("'" + message + "' Отправлено: " + member.name)
    #     channel = self.bot.get_channel(var.kBotMessage)
    #     emb = discord.Embed(description=f':incoming_envelope: **{ctx.author.mention}** отправил {member.mention}: ```{message}```',color = var.cSuccess)
    #     await channel.send( embed = emb )


    # # todo ОТПРАВИТЬ СООБЩЕНИЕ ОПРЕДЕЛЕННЫМ РОЛЯМ [от имени бота]
    # @commands.command( aliases = var.aRoleSend, brief = var.bRoleSend, usage = var.uRoleSend )
    # @commands.has_permissions( administrator = True )
    # async def __rolesend( self, ctx, role: discord.Role, *, message ):
    #     await ctx.message.delete()
    #     for member in role.members:
    #         try:
    #             await member.send( message )
    #             print("'" + message + "' Отправлено: " + member.name)
    #         except:
    #             print("Не могу отправить: '" + message + "'" + member.name)

    #     channel = self.bot.get_channel(var.kBotMessage)
    #     generation = [member.mention for member in role.members]
    #     emb = discord.Embed(description=f':incoming_envelope: **{ctx.author.mention}** отправил роли {role}: ```{message}```',color=var.cSuccess)
    #     emb.add_field(name="Пользователи с данной ролью:", value=f'**{", ".join(generation)}**', inline=False)
    #     await channel.send(embed=emb)




async def setup(bot):
    await bot.add_cog(Moder(bot))

print( 'Cogs - "Moder" connected' )