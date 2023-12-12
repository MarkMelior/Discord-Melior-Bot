    
from discord import SlashOption
import nextcord
from nextcord.ext import commands
import var
import config
from SQL import connection, cursor
from function import db_descBalance, deleteSlash
from config import transport, business, house, farm


cursor.execute( "DROP TABLE shop" )
cursor.execute( """CREATE TABLE IF NOT EXISTS shop (
    item_id BIGINT,
    item_type INT,
    cost BIGINT
)""" )

# 1 - Профессия
cursor.execute(f"INSERT INTO shop VALUES ({config.rMiddle}, 1, 32000)")
cursor.execute(f"INSERT INTO shop VALUES ({config.rSenior}, 1, 240000)")
# 2 - Канал доступ
cursor.execute(f"INSERT INTO shop VALUES ({config.rGopnik}, 2, 100000)")
cursor.execute(f"INSERT INTO shop VALUES ({config.rDemic}, 2, 100000)")
# 3 - Бусты
cursor.execute(f"INSERT INTO shop VALUES ({config.r2xBonus}, 3, 49400)")
cursor.execute(f"INSERT INTO shop VALUES ({config.rx5Casino}, 3, 180000)")
# 4 - Майнинг фермы
cursor.execute(f"INSERT INTO shop VALUES ({config.farm0}, 4, 58800)")
cursor.execute(f"INSERT INTO shop VALUES ({config.farm10}, 4, 199000)")
cursor.execute(f"INSERT INTO shop VALUES ({config.farm20}, 4, 725000)")
# 5 - Бизнес
cursor.execute(f"INSERT INTO shop VALUES ({config.bus0}, 5, 24500)")
cursor.execute(f"INSERT INTO shop VALUES ({config.bus10}, 5, 188000)")
cursor.execute(f"INSERT INTO shop VALUES ({config.bus20}, 5, 1250000)")
# 6 - Дом
cursor.execute(f"INSERT INTO shop VALUES ({config.house0}, 6, 180000)")
cursor.execute(f"INSERT INTO shop VALUES ({config.house10}, 6, 555000)")
cursor.execute(f"INSERT INTO shop VALUES ({config.house20}, 6, 7300000)")
# 7 - Транспорт (машина, самолёт, яхта)
cursor.execute(f"INSERT INTO shop VALUES ({config.car0}, 7, 368000)")
cursor.execute(f"INSERT INTO shop VALUES ({config.car10}, 7, 5580000)")
cursor.execute(f"INSERT INTO shop VALUES ({config.car20}, 7, 22700000)")


connection.commit()


class EcoShop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot





    @nextcord.slash_command( description = var.bShop )
    async def shop( self, ctx, select = SlashOption(name="select", choices={
        "💼 Профессии": 'work',
        "🔓 Доступ к каналам": 'channel',
        "🔥 Бусты": 'boost',
        "⚡️ Майнинг фермы": 'farm',
        "📊 Бизнесы": 'business',
        "🏠 Жильё": 'house',
        "🚗 Личный транспорт": 'transport'
        }) ):
        if select == None:
            title = 'Магазин ролей'
            cursor.execute( 'SELECT item_id, cost FROM shop' )
        elif select == 'work':
            title = 'Профессии'
            cursor.execute( 'SELECT item_id, cost FROM shop WHERE item_type = 1' )
        elif select == 'channel':
            title = 'Доступ к каналам'
            cursor.execute( 'SELECT item_id, cost FROM shop WHERE item_type = 2' )
        elif select == 'boost':
            title = 'Бусты'
            cursor.execute( 'SELECT item_id, cost FROM shop WHERE item_type = 3' )
        elif select == 'farm':
            title = 'Майнинг фермы'
            cursor.execute( 'SELECT item_id, cost FROM shop WHERE item_type = 4' )
        elif select == 'business':
            title = 'Бизнесы'
            cursor.execute( 'SELECT item_id, cost FROM shop WHERE item_type = 5' )
        elif select == 'house':
            title = 'Жильё'
            cursor.execute( 'SELECT item_id, cost FROM shop WHERE item_type = 6' )
        elif select == 'transport':
            title = 'Личный транспорт'
            cursor.execute( 'SELECT item_id, cost FROM shop WHERE item_type = 7' )
        
        embed = nextcord.Embed( title = f':crown: {title}', description = f'<#1094883300180512808> - возможности ролей', color = config.cMain )
        result = cursor.fetchall()
        for row in result:
            embed.add_field( name = f'Стоимость: { row[1] }$ :leaves:', value = f'Роль: { ctx.guild.get_role( row[0] ).mention }', inline = False )
        msg = await ctx.send( embed = embed )
        await deleteSlash(self, ctx, msg)


    @nextcord.slash_command( description = var.bShopBuy )
    async def buy( self, ctx, role: nextcord.Role ):
        cursor.execute( f'SELECT cost FROM shop WHERE item_id = {role.id}' )
        cost_role = cursor.fetchone()[0] 
        cursor.execute( f'SELECT cash FROM users WHERE id = {ctx.user.id}' )
        cash_user = cursor.fetchone()[0] 

        if role in ctx.user.roles:
            description = f'❌ { ctx.user.mention} у вас уже есть роль <@&{ role.id }>'
            await ctx.send( embed = nextcord.Embed( description = description, color = config.cError ) )

        elif role.id in farm and role.id in ctx.user.roles:
            description = f'❌ { ctx.user.mention} У вас уже есть майнинг ферма. Продайте старую, чтобы купить новую'
            await ctx.send( embed = nextcord.Embed( description = description, color = config.cError ) )
        
        elif role.id in business and role.id in ctx.user.roles:
            description = f'❌ { ctx.user.mention} У вас уже есть бизнес. Продайте старый, чтобы купить новый'
            await ctx.send( embed = nextcord.Embed( description = description, color = config.cError ) )
        
        elif role.id in house and role.id in ctx.user.roles:
            description = f'❌ { ctx.user.mention} У вас уже есть дом. Продайте старый, чтобы купить новый'
            await ctx.send( embed = nextcord.Embed( description = description, color = config.cError ) )
        
        elif role.id in transport and role.id in ctx.user.roles:
            description = f'❌ { ctx.user.mention} У вас уже есть транспорт. Продайте старый, чтобы купить новый'
            await ctx.send( embed = nextcord.Embed( description = description, color = config.cError ) )

        elif cost_role > cash_user:
            cursor.execute( f'SELECT cash FROM users WHERE id = {ctx.user.id}')
            description = f'❌ { ctx.user.mention } у вас недостаточно средств для покупки <@&{ role.id }> \n \n :moneybag: Ваш баланс составляет: **{ cursor.fetchone()[0] }$ :leaves:**'
            await ctx.send( embed = nextcord.Embed( description = description, color = config.cError ) )
        
        else:
            cursor.execute( f'SELECT cost FROM shop WHERE item_id = {role.id}')
            result = cursor.fetchone()[0]
            await ctx.user.add_roles( role )
            await ctx.send( embed = nextcord.Embed( title='Куплено!', description = f'''{ ctx.user.mention } вы успешно приобрели роль <@&{ role.id }>'''  + db_descBalance(ctx.user.id, f'UPDATE users SET cash = cash - {result} WHERE id = {ctx.user.id}'), color = config.cSuccess ).set_footer(text=f'Итого: -{result}$') )



    @nextcord.slash_command( description = var.bShopSell )
    async def sell( self, ctx, role: nextcord.Role ):
        if role not in ctx.user.roles:
            await ctx.send( embed = nextcord.Embed( description = f':x: { ctx.user.mention } у вас нет данной роли, чтобы её продать!', color = config.cError ) )
        else:
            await ctx.user.remove_roles( role )

            cursor.execute( f"SELECT cost FROM shop WHERE item_id = {role.id}" )
            cash2 = cursor.fetchone()[0] / 2
            await ctx.send( embed = nextcord.Embed( title='Продано!', description = f'''{ ctx.user.mention } вы успешно продали роль <@&{ role.id }>''' + db_descBalance(ctx.user.id, f"UPDATE users SET cash = cash + {cash2} WHERE id = {ctx.user.id}"), color = config.cSuccess ).set_footer(text=f'Итого: +{int(cash2)}$') )




def setup(bot):
	bot.add_cog(EcoShop(bot))
        
print( 'Cogs - "EcoShop" connected' )