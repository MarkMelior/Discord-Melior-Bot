import nextcord
from nextcord.ext import commands
import var
import config
import random
from function import deleteSlash, setAuthor


class Gift(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None


    # ОТПРАВИТЬ ПОДАРОК ПОЛЬЗОВАТЕЛЮ
    @nextcord.slash_command( description = var.bGift )
    async def gift(self, ctx, emoji, member: nextcord.Member, *, reason=None):
        
        img = ['https://i.pinimg.com/736x/61/70/02/61700216d0eab612ecc49c2a87743b82.jpg']
        random_img = random.randint(0, len(img) - 1)
        
        titl = ['А чё, так можно было?', 'Как же ему повезло', 'Вау, да ты гений']
        random_titl = random.randint(0, len(titl) - 1)

        if member == ctx.user:
            descText = f':gift: {ctx.user.mention} нельзя дарить подарки самому себе',
            coloo = config.cError,
            memberText = f':gift: {ctx.user.mention} подарил*(а)* вам **{emoji}**'
        elif reason == None:
            descText = f':gift: {ctx.user.mention} подарил*(а)* **{emoji}** пользователю {member.mention}',
            coloo = config.cMain,
            memberText = f':gift: {ctx.user.mention} подарил*(а)* вам **{emoji}**'
        else:
            descText = f':gift: {ctx.user.mention} подарил*(а)* **{emoji}** пользователю {member.mention} со словами: `{reason}`',
            coloo = config.cMain,
            memberText = f':gift: {ctx.user.mention} подарил*(а)* вам **{emoji}** со словами: `{reason}`'
        emb = nextcord.Embed( title = None, description = descText[0], color = coloo[0] )
        emb.set_image( url = img[random_img] )
        emb.set_footer( text = titl[random_titl] )
        await setAuthor(ctx, emb)
        # await setUserMessage(member, memberText, delete = None, color = var.cMain)
        msg = await ctx.send( embed = emb )
        await deleteSlash(self, ctx, msg)




def setup(bot):
    bot.add_cog(Gift(bot))
    print( 'Cogs - "Gift" connected' )