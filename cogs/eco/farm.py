from nextcord.ext import commands, tasks
import config
from SQL import cursor, connection


class Farm(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.charge_users.start()

    def cog_unload(self):
        self.charge_users.cancel()



    @tasks.loop(minutes = 60)
    async def charge_users( self ):
        try:
            for guild in self.bot.guilds:
                for user in guild.members:                
                    for role in user.roles:
                        if role.id in config.farm:
                            if role.id == config.farm0:
                                crypto = config.farm0Crypto
                            elif role.id == config.farm10:
                                crypto = config.farm10Crypto
                            elif role.id == config.farm20:
                                crypto = config.farm20Crypto
                            cursor.execute(f"UPDATE users SET crypto = crypto + {crypto} WHERE id = {user.id}")

                        elif role.id in config.business:
                            if role.id == config.bus0:
                                cash = config.bus0Cash
                            if role.id == config.bus10:
                                cash = config.bus10Cash
                            if role.id == config.bus20:
                                cash = config.bus20Cash
                            cursor.execute(f"UPDATE users SET business_cash = business_cash + {cash} WHERE id = {user.id}")
            connection.commit()
        except Exception as e:
            print(e)



def setup(bot):
    bot.add_cog(Farm(bot))

print( 'Cogs - "Farm" connected' )