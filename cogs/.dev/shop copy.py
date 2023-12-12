    
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



class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    cursor.execute( """CREATE TABLE IF NOT EXISTS shop (
        role_id BIGINT,
        cost BIGINT
    )""" )


    @commands.command( aliases = var.aShopAdd, brief = var.bShopAdd, usage = var.uShopAdd )
    @commands.has_permissions( administrator = True )
    async def __addrole( self, ctx, role: discord.Role, cost: int = 0 ):
        if cost < 1:
            msg = await ctx.send( embed = discord.Embed( description = f'{ ctx.message.author.mention } стоимость роли не может быть меньше **1$** :leaves:', color = var.cError ) )
            await deleteBtn(self,ctx,msg)
        else:
            cursor.execute(f'INSERT INTO shop VALUES({role.id}, {cost})')
            connection.commit()
            await ctx.message.add_reaction("✅")
            channel = self.bot.get_channel(var.kMain)
            await ctx.send( embed = discord.Embed( title=':new: Новая роль!', description = f'В магазин была добавлена новая роль: <@&{ role.id }> \n \n :money_with_wings: Стоимость: `{cost}$`', color = var.cSuccess ) )



    @commands.command( aliases = var.aShopRemove, brief = var.bShopRemove, usage = var.uShopRemove )
    @commands.has_permissions( administrator = True )
    async def __removerole( self, ctx, role: discord.Role ):
        cursor.execute( f'DELETE FROM shop WHERE role_id = {role.id}' )
        connection.commit()
        await ctx.message.add_reaction("✅")
        await ctx.send( embed = discord.Embed( description = f'Роль <@&{ role.id }> была удалена из магазина!', color = var.cError ) )



    @commands.command( aliases = var.aShop, brief = var.bShop, usage = var.uShop )
    async def __shop( self, ctx ):
        embed = discord.Embed( title = ':crown: Магазин ролей', description = f'<#1094883300180512808> - возможности ролей', color = var.cMain )
        cursor.execute( 'SELECT role_id, cost FROM shop' )
        result = cursor.fetchall()
        for row in result:
            embed.add_field( name = f'Стоимость: { row[1] }$ :leaves:', value = f'Роль: { ctx.guild.get_role( row[0] ).mention }', inline = False )
        await ctx.send( embed = embed )



    @commands.command( aliases = var.aShopBuy, brief = var.bShopBuy, usage = var.uShopBuy )
    async def __buyrole( self, ctx, role: discord.Role = None ):
        cursor.execute( f'SELECT cost FROM shop WHERE role_id = {role.id}' )
        cost_role = cursor.fetchone()[0] 
        cursor.execute( f'SELECT cash FROM users WHERE id = {ctx.author.id}' )
        cash_user = cursor.fetchone()[0] 

        if role in ctx.author.roles:
            await ctx.send( embed = discord.Embed( description = f':x: { ctx.message.author.mention} у вас уже есть роль <@&{ role.id }>', color = var.cError ) )

        elif cost_role > cash_user:
            await ctx.send( embed = discord.Embed( description = f''':x: { ctx.message.author.mention } у вас недостаточно средств для покупки <@&{ role.id }> \n \n :moneybag: Ваш баланс составляет: **{ cursor.execute( 'SELECT cash FROM users WHERE id = {}'.format( ctx.author.id ) ).fetchone()[0] }$ :leaves:**''', color = var.cError ) )

        else:
            await ctx.message.add_reaction("✅")
            await ctx.author.add_roles( role )

            cursor.execute( f'SELECT cost FROM shop WHERE role_id = {role.id}')
            result = cursor.fetchone()[0]

            await ctx.send( embed = discord.Embed( title='Куплено!', description = f'''{ ctx.message.author.mention } вы успешно приобрели роль <@&{ role.id }>'''  + db_descBalance(ctx.author.id, f'UPDATE users SET cash = cash - {result} WHERE id = {ctx.author.id}'), color = var.cSuccess ).set_footer(text=f'Итого: -{result}$') )



    @commands.command( aliases = var.aShopSell, brief = var.bShopSell, usage = var.uShopSell )
    async def __sellrole( self, ctx, role: discord.Role ):
        if role not in ctx.author.roles:
            await ctx.send( embed = discord.Embed( description = f':x: { ctx.message.author.mention } у вас нет данной роли, чтобы её продать!', color = var.cError ) )
        else:
            await ctx.message.add_reaction("✅")
            await ctx.author.remove_roles( role )

            cursor.execute( f"SELECT cost FROM shop WHERE role_id = {role.id}" )
            cash2 = cursor.fetchone()[0] / 2
            await ctx.send( embed = discord.Embed( title='Продано!', description = f'''{ ctx.message.author.mention } вы успешно продали роль <@&{ role.id }>''' + db_descBalance(ctx.author.id, f"UPDATE users SET cash = cash + {cash2} WHERE id = {ctx.author.id}"), color = var.cSuccess ).set_footer(text=f'Итого: +{int(cash2)}$') )





async def setup(bot):
	await bot.add_cog(Shop(bot))

print( 'Cogs - "Shop" connected' )