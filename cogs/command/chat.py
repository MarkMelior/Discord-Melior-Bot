from discord import SlashOption
import nextcord
from nextcord.ext import commands
import var
import config
import random
from function import deleteSlash, setAuthor
from nextcord.ext.commands import BucketType
from nextcord.ext.commands import cooldown


class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.count = 0

    # ДЕЙСТВИЯ В ЧАТЕ
    @nextcord.slash_command( description = var.bChat )
    @cooldown(1, 10, BucketType.user)
    async def chat( self, ctx, member: nextcord.Member, action = SlashOption(name="select", choices={
        "😬 Укусить": 'укусить',
        "💋 Поцеловать": 'поцеловать',
        "👊 Ударить": 'ударить',
        "😜 Облизать": 'облизать',
        "👏 шлепнуть": 'шлепнуть',
        "😌 Погладить": 'погладить',
        "🤗 Обнять": 'обнять',
        "😋 Съесть": 'съесть',
        "🖇 Связать": 'связать',
        "💨 Толкнуть": 'толкнуть',
        "🔔 Позвать": 'позвать',
        "💢 Выебать": 'выебать',
        }), *, text = None ):

        if action == 'укусить':
            smile = [':grin:']
            text = ['укусил']
            link = ['https://i.pinimg.com/originals/0f/7c/6b/0f7c6b2ff486a0953cb882876367e68e.jpg', 'https://coub-attachments.akamaized.net/coub_storage/coub/simple/cw_image/3f33ef5b32d/d5ede1d44530301fa305b/1507234657_00024.jpg']
            titl = ['Будешь знать']
            colo = None
        elif action  == 'поцеловать':
            smile = [':kiss:']
            text = ['поцеловал']
            link = ['https://i.pinimg.com/originals/a9/c7/25/a9c72512c779f2f574b3fc7a9061b0f9.png', 'https://media.moddb.com/images/groups/1/1/84/Konachan.com_-_52129_kiss_queen_bonjourno_sano_toshihide_seifuku.jpg', 'https://pibig.info/uploads/posts/2021-05/1619958081_25-pibig_info-p-tyan-i-kun-art-anime-krasivo-26.jpg', 'https://i.pinimg.com/originals/56/7a/57/567a579f540418f9d33c29662ed97be1.png']
            titl = ['Уььу']
            colo = None
        elif action  == 'ударить':
            smile = [':punch:']
            text = ['ударил', 'побил']
            link = ['https://static.mk.ru/upload/entities/2019/11/22/10/articles/facebookPicture/6a/b2/c4/bc/d89932470bc8a05786f57a363dd2a76e.jpg']
            titl = ['НАААААААА', 'ТУДА ЕГООО']
            colo = None
        elif action  == 'облизать':
            smile = [':tongue:']
            text = ['облизал']
            link = ['https://cs5.pikabu.ru/post_img/big/2015/03/02/11/1425320867_706142927.jpg']
            titl = ['Ого, извращенцы походу']
            colo = None
        elif action  == 'шлепнуть':
            smile = [':clap:']
            text = ['шлёпнул']
            link = ['']
            titl = ['Ого, извращенцы походу']
            colo = None
        elif action  == 'погладить':
            smile = [':hugging:']
            text = ['погладил']
            link = ['http://img10.reactor.cc/pics/post/full/Anime-Art-artist-Anime-Makuran-5545943.jpeg']
            titl = ['Хы']
            colo = None
        elif action  == 'обнять':
            smile = [':sparkles:']
            text = ['обнял']
            link = ['https://shutniki.club/wp-content/uploads/2019/11/Devushka_obnimaet_parnya_anime_8_29141310.jpg']
            titl = ['хЫ']
            colo = None
        elif action  == 'съесть':
            smile = [':stuck_out_tongue:']
            text = ['съел']
            link = ['https://static.zerochan.net/RedAkanekoCat.full.2888669.jpg']
            titl = ['Непонял. За что?']
            colo = None
        elif action  == 'связать':
            smile = [':paperclips:']
            text = ['связал']
            link = ['https://cdn.discordapp.com/attachments/848275413893513275/849222825637314610/1621824478403.jpg']
            titl = ['Долг не отдали хвхыфв']
            colo = None
        elif action  == 'толкнуть':
            smile = [':dash:']
            text = ['толкнул']
            link = ['https://cdn.discordapp.com/attachments/848275413893513275/849223512140021780/IMG_20210521_212312.jpg']
            titl = ['Оп оп, что-то намечается', 'Походу сейчас ему втащат', 'Ой зряяя']
            colo = None
        elif action  == 'позвать':
            smile = [':bell:']
            text = ['позвал', 'вызвал']
            link = ['']
            titl = ['А ну сюда подошёл!']
            colo = None
        elif action  == 'выебать':
            smile = [':anger:']
            text = ['выебал']
            link = ['https://static.zerochan.net/Sumeragi.Ayaka.full.1249023.jpg']
            titl = ['Воу воу, полегче']
            colo = 0xffff00

    
        random_link = random.randint(0, len(link) - 1)
        random_smile = random.randint(0, len(smile) - 1)
        random_text = random.randint(0, len(text) - 1)
        random_titl = random.randint(0, len(titl) - 1)

        if colo == None:
            colo = config.cMain

        descNoReason1 = f'{ smile[random_smile] } { ctx.user.mention } { text[random_text] }*(а)* { member.mention }'
        memberNoReason1 = f'{ smile[random_smile] } Тебя { text[random_text] }*(а)* { ctx.user.mention }'
        descNoReason2 = f'{ smile[random_smile] } { member.mention } { text[random_text] }*(а)* себя'


        if ctx.user == ctx.user and text == None:
            descText = descNoReason2
            memberText = None
        elif ctx.user == ctx.user:
            descText = descNoReason2 + f' со словами: `{ text }`',
            memberText = None
        elif text == None:
            descText = descNoReason1
            memberText = memberNoReason1
        else:
            descText = descNoReason1 + f' со словами: `{ text }`',
            memberText = memberNoReason1 + f' со словами: `{ text }`'
            

        emb = nextcord.Embed( title = None, description = descText[0], color = colo )
        emb.set_image( url = link[random_link] )
        emb.set_footer( text = titl[random_titl] )
        await setAuthor(ctx, emb)
        # await setUserMessage(member, memberText, delete = None, color = cMain)
        msg = await ctx.send( embed = emb )
        await deleteSlash(self, ctx, msg)

def setup(bot):
    bot.add_cog(Chat(bot))
    print( 'Cogs - "Chat" connected' )