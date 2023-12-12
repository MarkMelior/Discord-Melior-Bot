import nextcord
import var
import asyncio
from SQL import connection, cursor
import random
from config import *





# * CUSTOM ФУНКЦИЯ: EMBED
async def embed_func(
    desc = None, #ОСНОВНАЯ ИНФОРМАЦИЯ
    col = cMain, # ЦВЕТ EMBED
    title = None, # ЗАГОЛОВОК
    authorMsg = False, # ОТОБРАЗИТЬ АВТОРА, КОТОРЫЙ ВЫЗВАЛ КОМАНДУ
    field_name = None, field_value = None, # ИМЯ И ЗНАЧЕНИЕ
    img_url = None, # КАРТИНКА
    footer_text = None, # FOOTER ТЕКСТ

    deleteMsg = False, # УДАЛИТЬ СООБЩЕНИЕ АВТОРА
    deleteBtn = False, # УДАЛЕНИЕ СООБЩЕНИЯ НАЖАВ НА РЕАКЦИЮ
    deleteAuto = None, # АВТОМАТИЧЕСКОЕ УДАЛЕНИЕ ЧЕРЕЗ [время в секундах]

    reactionMsg = None, # ДОБАВИТЬ РЕАКЦИЮ НА СООБЩЕНИЕ АВТОРА [true=✅, false=❌]

    channelSend = None, # ОТПРАВИТЬ СООБЩЕНИЕ В КАНАЛ [id канала]
    MemberSend = None, # ОТПРАВИТЬ СООБЩЕНИЕ В ЛС [текст сообщения]
    MemberDelete = None, # УДАЛИТЬ ЧЕРЕЗ [время в секундах]

    # customCommand = None,
    cycleFieldEval = None, # техническая: только для команды `help`
    cycleFieldName = None, # кортеж ['', '']
    cycleFieldValue = None, # кортеж ['', '']

    self = None, ctx = None, member = None, # ТЕХНИЧЕСКИЕ КОММАНДЫ
    ):


    embed = nextcord.Embed( title = title, description = desc, color = col )
    # eval(customCommand)


    # ADD FIELD
    if cycleFieldEval != None:
        for i in cycleFieldEval:
            name = cycleFieldName + i
            value = cycleFieldValue + i
            embed.add_field( name = eval(name), value = eval(value), inline = False )
    if cycleFieldName != None and cycleFieldEval == None:
        for name, value in zip(cycleFieldName, cycleFieldValue):
            embed.add_field( name = name, value = value, inline = False )
                        

    # УДАЛИТЬ СООБЩЕНИЕ АВТОРА
    if deleteMsg == True:
        await ctx.message.delete()
    else:
        # ДОБАВИТЬ РЕАКЦИЮ НА СООБЩЕНИЕ АВТОРА [true=✅, false=❌]
        if reactionMsg == True:
            await ctx.message.add_reaction("✅")
        if reactionMsg == False:
            await ctx.message.add_reaction("❌")


    # ОТПРАВИТЬ СООБЩЕНИЕ В ЛС [текст сообщения]
    if MemberSend != None:
        sendmember = await member.send( embed = nextcord.Embed( description = MemberSend, color = col ), delete_after = MemberDelete )
    
    # КАРТИНКА
    if img_url != None:
        embed.set_image( url = img_url )

    # ОТОБРАЗИТЬ АВТОРА, КОТОРЫЙ ВЫЗВАЛ КОМАНДУ
    if authorMsg == True:
        embed.set_author( name = ctx.author, icon_url = ctx.author.avatar )

    # ИМЯ И ЗНАЧЕНИЕ
    if field_name != None:
        embed.add_field( name = field_name, value = field_value, inline = False )

    # FOOTER ТЕКСТ
    if footer_text != None:
        embed.set_footer( text = footer_text )

    # ОТПРАВИТЬ СООБЩЕНИЕ В КАНАЛ [id канала]
    if channelSend != None:
        channel = self.bot.get_channel( channelSend )
        msg = await channel.send( embed = embed, delete_after = deleteAuto )
    else:
        msg = await ctx.send( embed = embed, delete_after = deleteAuto )

    # УДАЛЕНИЕ СООБЩЕНИЯ НАЖАВ НА РЕАКЦИЮ
    if deleteBtn == True:
        # await msg.add_reaction("🗑️") # Реакция на сообщение отправленное ботом
        # full_msg = await msg.fetch()
        # await full_msg.add_reaction("🗑️") # Реакция на сообщение автора

        def check( reaction, user ):
            #если пользователь является автором сообщения/владельцем сервера и поставил реакцию, то:
            return (user == ctx.user or user == ctx.guild.owner_id) and str( reaction.emoji ) == '🗑️'
        try:
            await self.bot.wait_for('reaction_add', timeout = 60, check = check )
        #если время вышло, то:
        except asyncio.TimeoutError:
            return 
        else:
            await msg.delete()
            if MemberSend != None:
                await sendmember.delete()
            if deleteMsg != True:
                await ctx.message.delete()

    return









# * TEMPLATE: ФУНКЦИИ ЗАПРОСОВ ИЗ БАЗЫ ДАННЫХ
#баланс пользователя
def db_balance_user(id_user):
    cursor.execute(f"SELECT cash FROM users WHERE id = {id_user}") 
    return cursor.fetchone()[0]
#опыт пользователя
def db_xp_user(id_user):
    cursor.execute(f"SELECT xp FROM users WHERE id = {id_user}") 
    return cursor.fetchone()[0]
#уровень пользователя
def db_lvl_user(id_user):
    cursor.execute(f"SELECT lvl FROM users WHERE id = {id_user}") 
    return cursor.fetchone()[0]

# БАЛАНС И ОПЫТ: BEFORE & AFTER
def db_descBalance(id_user, evt, xp = False):
    balance_user = db_balance_user(id_user)
    if xp == True:
        xp_user = db_xp_user(id_user)

    cursor.execute(evt)
    connection.commit()

    balance_user_new = db_balance_user(id_user)
    if xp == True:
        xp_user_new = db_xp_user(id_user)


    descBalance = f'\n \n :moneybag: Баланс: {balance_user}$ -> **{balance_user_new}$ :leaves:**'

    if xp == True:
        descXp = f'\n :sparkles: Опыт: {xp_user}xp -> **{xp_user_new}xp**'
        return descBalance + descXp
    else:
        return descBalance

        


async def deleteSlash(self, ctx, msg):
    full_msg = await msg.fetch()
    await full_msg.add_reaction("🗑️")

    def check( reaction, user ):
        return (user == ctx.user or user == ctx.guild.owner_id) and str( reaction.emoji ) == '🗑️'
    try:
        await self.bot.wait_for('reaction_add', timeout = 10, check = check )
    except asyncio.TimeoutError:
        await full_msg.clear_reactions()
        return 
    else:
        await msg.delete()


# * TEMPLATE: да
# function.delete_btn(self, ctx, msg, MemberSend = None, deleteMsg = False)
async def deleteBtn(self, ctx, msg):
    await msg.add_reaction("🗑️") # Реакция на сообщение автора

    def check( reaction, user ):
        #если пользователь является автором сообщения/владельцем сервера и поставил реакцию, то:
        return (user == ctx.message.author or user == ctx.guild.owner_id) and str( reaction.emoji ) == '🗑️'
    try:
        await self.bot.wait_for('reaction_add', timeout = 10, check = check )
    #если время вышло, то:
    except asyncio.TimeoutError:
        await ctx.message.clear_reactions()
        return 
    else:
        await msg.delete()
        await ctx.message.delete()


#Добавить автора сообщения
async def setAuthor(ctx, emb):
    emb.set_author( name = ctx.user, icon_url = ctx.user.avatar )


# ДОБАВИТЬ РЕАКЦИЮ НА СООБЩЕНИЕ АВТОРА [true=✅, false=❌]
async def setReaction(ctx, React = True):
        if React == True:
            await ctx.message.add_reaction("✅")
        if React == False:
            await ctx.message.add_reaction("❌")


# ОТПРАВИТЬ СООБЩЕНИЕ В ЛС [текст сообщения]
async def setUserMessage(member, text, delete = None, color = cMain):
    await member.send(
        embed = nextcord.Embed( description = text, color = color ), delete_after = delete
        )
    
# # ОТПРАВИТЬ СООБЩЕНИЕ В КАНАЛ [id канала]
# async def setChannel(self, ctx, ID = None, delete = None):
#     if ID != None:
#         channel = self.bot.get_channel( ID )
#         await channel.send( embed = embed, delete_after = delete )
#     else:
#         await ctx.send( embed = embed, delete_after = delete )





# ПРОВЕРКА НА НОВЫЙ УРОВЕНЬ
async def msgXp(msg):
    cursor.execute(f"SELECT xp, lvl FROM users WHERE id={msg.id}")
    result = cursor.fetchone()
    xp = result[0]
    level = result[1]
    lvch = xp / ((level * 1.5) * 1000)
    if level < lvch: #если текущий уровень меньше уровня, который был рассчитан формулой выше,...
        bal = int(2000 * lvch)
        embed = nextcord.Embed( title = f':partying_face: Новый уровень!', description = f'{msg.mention} теперь у тебя `{level+1} lvl`!'+db_descBalance(msg.id, f'UPDATE users SET lvl=lvl+1, cash=cash+{bal} WHERE id={msg.id}'), color = cSuccess )
        embed.set_footer(text=f'начислено +{bal}$')
        await msg.channel.send( embed = embed )

    connection.commit()#применение изменений в БД