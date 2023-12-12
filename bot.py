import nextcord
from nextcord.ext import commands

import aiohttp
import io
import openai

import var
from config import *
from SQL import connection, cursor

openai.api_key = OPENAI_KEY


#СПИСОК COGS ДЛЯ ПОДКЛЮЧЕНИЯ
extensions = [
    # COMMAND
    'cogs.command.chat',
    'cogs.command.gift',
    'cogs.command.serverStats',
    'cogs.command.help',

    # ECO
    'cogs.eco.balance',
    'cogs.eco.bonus',
    'cogs.eco.casino',
    'cogs.eco.pay',
    'cogs.eco.shop',
    'cogs.eco.top',
    'cogs.eco.user',
    'cogs.eco.work',
    'cogs.eco.farm',

    # EVENT
    'cogs.event.error',
    'cogs.event.join',
    'cogs.event.reactionEmoji',
    'cogs.event.blockPrivateMsg',
    'cogs.event.xpMsg',

    # ADMIN
    'cogs.admin.TakeAward',
    'cogs.admin.clear',
]

#ПАРАМЕТРЫ БОТА
intents = nextcord.Intents.all()
intents.message_content = True
client = commands.Bot( command_prefix = PREFIX, intents = intents, default_guild_ids=TESTING_GUILD_ID )
client.remove_command( 'help' )


#ФУНКЦИЯ БД: ДОБАВЛЕНИЕ НОВОГО ПОЛЬЗОВАТЕЛЯ
def add_users(member):
    cursor.execute(f"SELECT id FROM users WHERE id = {member.id}") #проверка, существует ли участник в БД
    if cursor.fetchone() == None: #Если не существует
        cursor.execute(f"INSERT INTO users VALUES ({member.id}, '{member.name}', 0, 1, 500, 0, 0, 0)") #вводит все данные об участнике в БД
    else: #если существует
        pass
    connection.commit() #применение изменений в БД

# #ФУНКЦИЯ БД: ПРОВЕКА ПОЛЬЗОВАТЕЛЯ НА БАН, МУТ
# async def check_users(ctx, member):
#     banned = cursor.execute(f"SELECT banned FROM users WHERE id = {member.id}")[0]
#     muted = cursor.execute(f"SELECT muted FROM users WHERE id = {member.id}")[0]
#     if banned == 1:
#         await member.add_roles(discord.utils.get(ctx.message.guild.roles, id = rBan))
#     elif muted == 1:
#         await member.add_roles(discord.utils.get(ctx.message.guild.roles, id = rMute))
#     else:
#         pass

#ИВЕНТ: ПРИСОЕДИНЕНИЕ ПОЛЬЗОВАТЕЛЯ
@client.event
async def on_member_join(member):
    add_users(member) # функция дб
    # check_users(ctx, member) # функция дб 

# ЗАГРУЗКА COGS
if __name__ == '__main__':
    for ext in extensions:
        try:
            client.load_extension(ext)
        except Exception as e:
            print(f"error while loading {ext} \n {e}")

#ИВЕНТ: ЗАПУСК БОТА
@client.event
async def on_ready():

    #БАЗА ДАННЫХ
    # cursor.execute( "DROP TABLE users" )
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        id bigint,
        nikname text,
        xp int,
        lvl int,
        cash bigint,
        business_cash BIGINT,
        crypto BIGINT,
        msg INT
        );""")
    connection.commit()


    #БАЗА ДАННЫХ: ДОБАВЛЕНИЕ НОВОГО ПОЛЬЗОВАТЕЛЯ
    for guild in client.guilds: #т.к. бот для одного сервера, то и цикл выводит один сервер
        print('ID Сервера: ', guild.id) #вывод id сервера
        for user in guild.members: #цикл, обрабатывающий список участников
            add_users(user) # БАЗА ДАННЫХ: ДОБАВЛЕНИЕ НОВОГО ПОЛЬЗОВАТЕЛЯ


    #ПАРАМЕТРЫ БОТА AWAIT
    await client.change_presence( status = nextcord.Status.online, activity = nextcord.Game( '{}{}'.format( PREFIX, var.aHelp[0] ) ) )

    # channel = client.get_channel( kLog )
    # await channel.send( embed = discord.Embed(description=f':white_check_mark: **Бот успешно запущен!**', color = cSuccess))


    #ВЫДАЧА ДЕНЕГ С БИЗНЕСА
    # while True:
    #     # retrieve user IDs and cash balances from the users table
    #     cursor.execute("SELECT id, cash FROM users")
    #     rows = cursor.fetchall()
    #     if rows[0] in business:
    #         print('DONE')
        
        # for row in rows:
        #     user_id = row[0]
        #     if user_id in business:
        #         cash_balance = row[1]
        #         new_balance = cash_balance + 100
        #         cursor.execute("UPDATE users SET business_cash = business_cash + ? WHERE id = ?", (new_balance, user_id))
        #         connection.commit()
        # time.sleep(3600)


    print( 'Bot connected' )


#ИВЕНТ: СООБЩЕНИЯ
@client.event
async def on_message( msg: nextcord.Message ):

    # Нейросеть txt to txt
    if msg.channel.id == kTxtToTxt and not msg.author.bot:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=msg.content,
            temperature=0.5,
            max_tokens=1000,
            top_p=1.0,
            frequency_penalty=0.5,
            presence_penalty=0.0,
            # stop=["you:"]
        )

        await msg.channel.send(response['choices'][0]['text'])

    # Нейросеть txt to img
    if msg.channel.id == kTxtToImg and not msg.author.bot:
        response = openai.Image.create(
            prompt=msg.content,
            n=1,
            size="512x512"
        )
        await msg.channel.send(response['data'][0]['url'])

    try:
        # Нейросеть в стиле гопника
        if msg.channel.id == kGopnik and not msg.author.bot:
            response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                    {"role": "system", "content": "Answer like a gopnik. "},
                    {"role": "user", "content": msg.content},
                ]
            )
            await msg.channel.send(response['choices'][0]['message']['content'])
    except Exception as e:
        print(e)

    # Демотиватор 2.0
    if msg.channel.id == kDemotivator and not msg.author.bot:
        from PIL import ImageFont
        from PIL import Image
        from PIL import ImageDraw

        if msg.attachments:
            attachment = msg.attachments[0]
            if attachment.filename.endswith(".jpg") or attachment.filename.endswith(".jpeg") or attachment.filename.endswith(".png") or attachment.filename.endswith(".webp"):
                if msg.content:
                    url = str(msg.attachments[0]) # must be an image
                    async with aiohttp.ClientSession() as session: # creates session
                        async with session.get(url) as resp: # gets image from url
                            img = await resp.read() # reads image from response
                            with io.BytesIO(img) as file: # converts to file-like object
                                # await msg.channel.send(file=discord.File(file, "testimage.png"))
                                template = Image.open('assets/demotivator/template.jpg')
                                mem = Image.open(file).convert('RGBA')
                                text = msg.content

                                width = 610
                                height = 569
                                resized_mem = mem.resize((width, height), Image.ANTIALIAS)

                                text_position = (0, 0)
                                text_color = (266,0,0)


                                strip_width, strip_height = 700, 1300

                                def findLen(text_len):
                                    counter = 0    
                                    for i in text_len:
                                        counter += 1
                                    return counter

                                font_width = 60
                                
                                if findLen(text) >= 25:
                                    font_width = 50

                                background = Image.new('RGB', (strip_width, strip_height)) #creating the black strip
                                draw = ImageDraw.Draw(template)

                                if '\n' in text:  
                                    split_offers = text.split('\n')

                                    for i in range(2):
                                        if i == 1:
                                            strip_height += 110
                                            font_width -= 20
                                        font = ImageFont.truetype("assets/demotivator/font.ttf", font_width) 
                                        text_width, text_height = draw.textsize(split_offers[i], font)

                                        position = ((strip_width-text_width)/2,(strip_height-text_height)/2)
                                        draw.text(position, split_offers[i], font=font)
                                else:
                                    font = ImageFont.truetype("assets/demotivator/font.ttf", font_width)
                                    text_width, text_height = draw.textsize(text, font)
                                    strip_height = 1330
                                    position = ((strip_width-text_width)/2,(strip_height-text_height)/2)
                                    draw.text(position, text, font=font)


                                template.paste(resized_mem, (54, 32),  resized_mem)
                                buffer = io.BytesIO()
                                template.save(buffer, format='JPEG', quality=75)
                                buffer.seek(0)

                                await msg.delete()
                                emb = nextcord.Embed( description = f'{msg.author.mention} Ваш демик готов!', color = 0xd7d7d7 )
                                emb.set_author( name = msg.author, icon_url = msg.author.avatar )
                                emb.set_footer(text = f'Текст: {msg.content}')
                                emb.set_image(url="attachment://MeliorLive.jpeg")
                                await msg.channel.send( file = nextcord.File(buffer, "MeliorLive.jpeg"), embed = emb )
                                return
                else:
                    await msg.delete()
                    emb = nextcord.Embed( description = '❌ Ты забыл добавить подпись', color = cError )
                    emb.set_author( name = msg.author, icon_url = msg.author.avatar )
                    await msg.channel.send( embed = emb, delete_after = 10 )
                    return
            else:
                await msg.delete()
                emb = nextcord.Embed( description = '❌ Неверный формат фото! ```Поддерживаемые форматы: [.jpg, .png, .jpeg, .webp]```', color = cError )
                emb.set_author( name = msg.author, icon_url = msg.author.avatar )
                await msg.channel.send( embed = emb, delete_after = 10 )
        else:
            await msg.delete()
            emb = nextcord.Embed( description = 'Отправь мне фото с подписью', color = cError )
            emb.set_author( name = msg.author, icon_url = msg.author.avatar )
            await msg.channel.send( embed = emb, delete_after = 10 )

    # # ОБРАБОТКА КАРТИНКИ
    # if msg.channel.id == 1093447086395097169 and not msg.author.bot:
    #     import torch
    #     await msg.add_reaction("✅")
    #     from PIL import Image
    #     model = torch.hub.load("bryandlee/animegan2-pytorch:main", "generator", pretrained="face_paint_512_v2")
    #     face2paint = torch.hub.load("bryandlee/animegan2-pytorch:main", "face2paint", size=512)

    #     url = str(msg.attachments[0]) # must be an image
    #     async with aiohttp.ClientSession() as session: # creates session
    #         async with session.get(url) as resp: # gets image from url
    #             img = await resp.read() # reads image from response
    #             with io.BytesIO(img) as file: # converts to file-like object
    #                 img = Image.open(file).convert('RGB')
    #                 buffer = io.BytesIO()
    #                 face2paint(model, img).save(buffer, format='JPEG', quality=80)
    #                 buffer.seek(0)

    #                 emb = discord.Embed( description = f'{msg.author.mention} Ваше изображение готово!', color = 0xd7d7d7 )
    #                 emb.set_author( name = msg.author, icon_url = msg.author.avatar )
    #                 emb.set_image(url="attachment://MeliorLive.jpeg")

    #                 await msg.channel.send(file = discord.File(buffer, "MeliorLive.jpeg"), embed = emb )


# ЗАПУСК БОТА
client.run( TOKEN )