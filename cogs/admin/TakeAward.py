import nextcord
from nextcord.ext import commands
import var
import config
from SQL import connection, cursor
from function import deleteSlash, db_descBalance, setAuthor
from nextcord.ext import application_checks

class EcoTakeAward(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    # НАЧИСЛИТЬ ДЕНЬГИ
    @nextcord.slash_command( description = var.bGameAward )
    @application_checks.is_owner()
    async def award( self, ctx, member: nextcord.Member, cash ):

        if cash < 1:
            emb = nextcord.Embed( description = f':x: {ctx.user.mention} укажи сумму больше 1$ :leaves:', color = config.cError )
            # await setAuthor(ctx, emb)
            msg = await ctx.send( embed = emb, delete_after = 10 )
            full_msg = await msg.fetch()
            await full_msg.add_reaction("❌")
            await deleteSlash(self, ctx, msg)

        else:
            balance = db_descBalance(member.id, f"UPDATE users SET cash = cash + {cash} WHERE id = {member.id}")
            emb = nextcord.Embed( description = f'На счёт {member.mention} было зачислено: **{cash}$** :leaves:' + balance, color = config.cSuccess )
            msg = await ctx.send( embed = emb )
            await member.send( embed = nextcord.Embed( description = f'На ваш счёт было зачислено: **{cash}$** :leaves: от {ctx.user.mention}' + balance, color = config.cSuccess ) )
            await deleteSlash(self, ctx, msg)
    
    
    # СПИСАТЬ ДЕНЬГИ
    @nextcord.slash_command( description = var.bGameTake )
    @application_checks.is_owner()
    async def take( self, ctx, member: nextcord.Member, cash ):
        if cash in ['all', 'все', 'всё']:
            cursor.execute(f"UPDATE users SET cash = 0 WHERE id = {member.id}")
            connection.commit()

            emb = nextcord.Embed( description = f'{member.mention} счёт аннулирован :leaves: \n \n :moneybag: баланс пользователя составляет: **0$ :leaves:**', color = config.cError )
            # await setAuthor(ctx, emb)
            msg = await ctx.send( embed = emb )
            await member.send( embed = nextcord.Embed( description = f'Ваш счёт аннулирован :leaves: \n \n :moneybag: Ваш баланс составляет: **0$ :leaves:**', color = config.cError ) )
            await deleteSlash(self, ctx, msg)


        elif cash < 1:
            emb = nextcord.Embed( description = f'{ctx.uset.mention} укажи сумму больше **1$** :leaves:', color = config.cError )
            # await setAuthor(ctx, emb)
            msg = await ctx.send( embed = emb, delete_after = 10 )
            await deleteSlash(self, ctx, msg)

        else:
            cursor.execute(f"UPDATE users SET cash = cash - {cash} WHERE id = {member.id}")
            connection.commit()
            cursor.execute(f"SELECT cash FROM users WHERE id = {member.id}")
            balance = cursor.fetchone()[0]

            emb = nextcord.Embed( description = f'У {member.mention} списали: **{cash}$** :leaves: \n \n :moneybag: баланс пользователя составляет: **{balance}$ :leaves:**', color = config.cError )
            # await setAuthor(ctx, emb)
            msg = await ctx.send( embed = emb )
            await member.send( embed = nextcord.Embed( description = f'У вас списали: **{cash}$** :leaves: \n \n :moneybag: Ваш баланс составляет: **{balance}$ :leaves:**', color = config.cError ) )
            await deleteSlash(self, ctx, msg)



    # # НАЧИСЛИТЬ ОПЫТ
    # # @nextcord.slash_command( description = var.bGameAward )
    # @commands.command()
    # @application_checks.is_owner()
    # async def awardxp( self, ctx, member: nextcord.Member, xp ):

    #     if xp < 1:
    #         emb = nextcord.Embed( description = f':x: {ctx.user.mention} укажи опыт больше 1', color = config.cError )
    #         # await setAuthor(ctx, emb)
    #         msg = await ctx.send( embed = emb, delete_after = 10 )
    #         full_msg = await msg.fetch()
    #         await full_msg.add_reaction("❌")
    #         await deleteSlash(self, ctx, msg)

    #     else:
    #         balance = db_descBalance(member.id, f"UPDATE users SET xp = xp + {xp} WHERE id = {member.id}")
    #         emb = nextcord.Embed( description = f'На счёт {member.mention} было зачислено: **{xp}**', color = config.cSuccess )
    #         msg = await ctx.send( embed = emb )
    #         # await member.send( embed = nextcord.Embed( description = f'На ваш счёт было зачислено: **{xp}$** :leaves: от {ctx.user.mention}' + balance, color = config.cSuccess ) )
    #         await deleteSlash(self, ctx, msg)
    
    
    # # СПИСАТЬ ОПЫТ
    # # @nextcord.slash_command( description = var.bGameTake )
    # @commands.command()
    # @application_checks.is_owner()
    # async def takexp( self, ctx, member: nextcord.Member, xp ):
    #     if xp in ['all', 'все', 'всё']:
    #         cursor.execute(f"UPDATE users SET xp = 0 WHERE id = {member.id}")
    #         connection.commit()

    #         emb = nextcord.Embed( description = f'{member.mention} опыт аннулирован  \n \n опыт пользователя составляет: **0**', color = config.cError )
    #         msg = await ctx.send( embed = emb )
    #         # await member.send( embed = nextcord.Embed( description = f'Ваш счёт аннулирован :leaves: \n \n :moneybag: Ваш баланс составляет: **0$ :leaves:**', color = config.cError ) )
    #         await deleteSlash(self, ctx, msg)


    #     elif xp < 1:
    #         emb = nextcord.Embed( description = f'{ctx.uset.mention} укажи опыт больше **1**', color = config.cError )
    #         msg = await ctx.send( embed = emb, delete_after = 10 )
    #         await deleteSlash(self, ctx, msg)

    #     else:
    #         cursor.execute(f"UPDATE users SET xp = xp - {xp} WHERE id = {member.id}")
    #         connection.commit()
    #         cursor.execute(f"SELECT xp FROM users WHERE id = {member.id}")
    #         balance = cursor.fetchone()[0]

    #         emb = nextcord.Embed( description = f'У {member.mention} списали: **{xp}** \n \n :moneybag: опыт пользователя составляет: **{balance}**', color = config.cError )
    #         msg = await ctx.send( embed = emb )
    #         # await member.send( embed = nextcord.Embed( description = f'У вас списали: **{xp}$** :leaves: \n \n :moneybag: Ваш баланс составляет: **{balance}$ :leaves:**', color = config.cError ) )
    #         await deleteSlash(self, ctx, msg)




def setup(bot):
    bot.add_cog(EcoTakeAward(bot))

print( 'Cogs - "EcoTakeAward" connected' )