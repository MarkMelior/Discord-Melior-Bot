import discord
from discord.ext import commands
import time
from pymongo import MongoClient
import var


class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prev = []
        self.cluster = MongoClient(var.MONGO_CLIENT)
        self.collection = self.cluster.ecodb.colldb

        global tdict
        tdict = {}



    @commands.Cog.listener()
    async def on_voice_state_update( self, member, before, after ):

        data = self.collection.find_one({"_id": member.id})
        print(data['voicetime'])

        author = member.id
        if before.channel is None and after.channel is not None:
            t1 = time.time()
            self.collection.update_one({"_id": member.id},
                                       {"$set": {"voicetime": t1}})
            tdict[author] = t1
        elif before.channel is not None and after.channel is None and author in int(data['voicetime']):
            t2 = time.time()
            self.collection.update_one({"_id": member.id},
                                       {"$set": {"voicetime": t2 - data['voicetime']}})
            print(t2 - tdict[author])



def setup(bot):
    bot.add_cog(Voice(bot))

print( 'Cogs - "Voice" connected' )