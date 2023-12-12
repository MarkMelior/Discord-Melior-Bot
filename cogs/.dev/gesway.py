import discord
from discord.ext import commands
import var
import random
from function import embed_func
from var import connection, cursor




try:
    #БАЗА ДАННЫХ: USER
    cursor.execute("""CREATE TABLE IF NOT EXISTS gesway (
        id bigint NOT NULL PRIMARY KEY,
        nikname text,
        xp int,
        lvl int,
        passed int
        );""")

    #БАЗА ДАННЫХ: ТЕКСТ
    cursor.execute("""CREATE TABLE IF NOT EXISTS gesway_action (
        id bigint NOT NULL,
        datetime DATETIME,
        action text,
        xp int,
        FOREIGN KEY (id) REFERENCES gesway(id) 
        ) ENGINE=INNODB;""")

    connection.commit()

except Exception as e:
    print(f"error gesway: {e}")






class Gesway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def gesreg( self, ctx ):
        try:
            cursor.execute(f"SELECT id FROM gesway WHERE id = {ctx.author.id}") #проверка, существует ли участник в БД
            if cursor.fetchone() == None: #Если не существует
                
                
                
                expStart = 100
                cursor.execute(f"INSERT INTO gesway (id, nikname, xp, lvl, passed) VALUES ({ctx.author.id}, '{ctx.author.name}', 0, 0, 0)")
                cursor.execute(f"INSERT INTO gesway_action (id, datetime, action, xp) VALUES ({ctx.author.id}, CURTIME(), 'Зарегестрировался в Gesway', {expStart})")
                cursor.execute(f"UPDATE gesway SET xp = xp + {expStart} WHERE id = {ctx.author.id}") #проверка, существует ли участник в БД
                connection.commit()
                
                
                
                await embed_func(
                    desc = f'{ctx.author.mention} вы были успешно зарегистрированы. Вам было зачислено **`+100xp`** за регистрацию. Поздравляю :D', #ОСНОВНАЯ ИНФОРМАЦИЯ
                    col = var.cSuccess, # ЦВЕТ EMBED
                    # title = None, # ЗАГОЛОВОК
                    authorMsg = True, # ОТОБРАЗИТЬ АВТОРА, КОТОРЫЙ ВЫЗВАЛ КОМАНДУ
                    # field_name = None, field_value = None, # ИМЯ И ЗНАЧЕНИЕ
                    # img_url = None, # КАРТИНКА
                    footer_text = var.gesFooter, # FOOTER ТЕКСТ

                    # deleteMsg = False, # УДАЛИТЬ СООБЩЕНИЕ АВТОРА
                    # deleteBtn = False, # УДАЛЕНИЕ СООБЩЕНИЯ НАЖАВ НА РЕАКЦИЮ
                    # deleteAuto = None, # АВТОМАТИЧЕСКОЕ УДАЛЕНИЕ ЧЕРЕЗ [время в секундах]

                    reactionMsg = True, # ДОБАВИТЬ РЕАКЦИЮ НА СООБЩЕНИЕ АВТОРА [true=✅, false=❌]

                    # ? channelSend = None, # ОТПРАВИТЬ СООБЩЕНИЕ В КАНАЛ [id канала]
                    # ? MemberSend = None, # ОТПРАВИТЬ СООБЩЕНИЕ В ЛС [текст сообщения]
                    # MemberDelete = None, # УДАЛИТЬ ЧЕРЕЗ [время в секундах]

                    # customCommand = None,
                    # cycleFieldEval = None, # техническая: только для команды `help`
                    # cycleFieldName = None, # кортеж ['', '']
                    # cycleFieldValue = None, # кортеж ['', '']

                    self = self, ctx = ctx, member = None, # ТЕХНИЧЕСКИЕ КОММАНДЫ
                    )

            else: #если существует
                await embed_func(
                    desc = f'{ctx.author.mention} вы уже зарегистрированы', #ОСНОВНАЯ ИНФОРМАЦИЯ
                    col = var.cError, # ЦВЕТ EMBED
                    # title = None, # ЗАГОЛОВОК
                    authorMsg = True, # ОТОБРАЗИТЬ АВТОРА, КОТОРЫЙ ВЫЗВАЛ КОМАНДУ
                    # field_name = None, field_value = None, # ИМЯ И ЗНАЧЕНИЕ
                    # img_url = None, # КАРТИНКА
                    footer_text = var.gesFooter, # FOOTER ТЕКСТ

                    # deleteMsg = False, # УДАЛИТЬ СООБЩЕНИЕ АВТОРА
                    deleteBtn = True, # УДАЛЕНИЕ СООБЩЕНИЯ НАЖАВ НА РЕАКЦИЮ
                    deleteAuto = 10, # АВТОМАТИЧЕСКОЕ УДАЛЕНИЕ ЧЕРЕЗ [время в секундах]

                    reactionMsg = False, # ДОБАВИТЬ РЕАКЦИЮ НА СООБЩЕНИЕ АВТОРА [true=✅, false=❌]

                    # channelSend = None, # ОТПРАВИТЬ СООБЩЕНИЕ В КАНАЛ [id канала]
                    # MemberSend = None, # ОТПРАВИТЬ СООБЩЕНИЕ В ЛС [текст сообщения]
                    # MemberDelete = None, # УДАЛИТЬ ЧЕРЕЗ [время в секундах]

                    # customCommand = None,
                    # cycleFieldEval = None, # техническая: только для команды `help`
                    # cycleFieldName = None, # кортеж ['', '']
                    # cycleFieldValue = None, # кортеж ['', '']

                    self = self, ctx = ctx, member = None, # ТЕХНИЧЕСКИЕ КОММАНДЫ
                    )
                pass
            connection.commit() #применение изменений в БД
        except Exception as e:
            print(f"error gesREG: {e}")







    @commands.command()
    async def gesday( self, ctx, day = 'DAYOFMONTH(NOW())', month = 'MONTH(NOW())', year = 'YEAR(NOW())' ):
        # print('+[gesday] (day) (mounth) (year)')

        date = f' AND DAYOFMONTH(`datetime`) = {day} AND MONTH(`datetime`) = {month} AND YEAR(`datetime`) = {year}'

        #ДАТА + ДАННЫЕ
        cursor.execute(f"SELECT DAYOFMONTH(`datetime`), MONTH(`datetime`), YEAR(`datetime`), SUM(xp) FROM gesway_action WHERE id = {ctx.author.id} {date}")
        data = cursor.fetchone()
        when = f'`{data[0]}.{data[1]}.{data[2]}`'

        #ЕСЛИ ПОЛЕ day == ВЧЕРА
        if day in ['вчера']:
            # day = int(day) - 1
            when = f'вчера ({when})'

        # СЕГОДНЯ
        if day == 'DAYOFMONTH(NOW())':
            when = f'сегодня ({when})'

        #ЕСТЬ ЛИ ВЫПОЛНЕННЫЕ ДЕЛА?
        cursor.execute(f"SELECT action, xp, TIME_FORMAT(`datetime`, '%H:%i') FROM gesway_action WHERE id = {ctx.author.id} {date}")
        result = cursor.fetchall()
        if result == ():
            await ctx.send(f'Ты лох ебаный. За `{when}` ты ничего не сделал')
            return

        #СПИСОК ВЫПОЛНЕННЫХ ДЕЛ (ЦИКЛ)
        inf = []
        time = []
        n = 0
        for i in result:
            n += 1
            inf.append(f'{n}. {i[0]} **`[+{i[1]}exp]`**')
            time.append(f'В {i[2]}')
        

        await embed_func(
            desc = f'''
```css
Всего опыта [+{data[3]}exp]
```
**Выполненные дела за {when}:**
            ''', #ОСНОВНАЯ ИНФОРМАЦИЯ
            col = var.gesColorMain, # ЦВЕТ EMBED
            # title = f'Выполненные дела за {when}: ', # ЗАГОЛОВОК
            authorMsg = True, # ОТОБРАЗИТЬ АВТОРА, КОТОРЫЙ ВЫЗВАЛ КОМАНДУ
            # field_name = None, field_value = None, # ИМЯ И ЗНАЧЕНИЕ
            # img_url = None, # КАРТИНКА
            footer_text = var.gesFooter, # FOOTER ТЕКСТ

            # deleteMsg = False, # УДАЛИТЬ СООБЩЕНИЕ АВТОРА
            deleteBtn = True, # УДАЛЕНИЕ СООБЩЕНИЯ НАЖАВ НА РЕАКЦИЮ
            # deleteAuto = 10, # АВТОМАТИЧЕСКОЕ УДАЛЕНИЕ ЧЕРЕЗ [время в секундах]

            reactionMsg = True, # ДОБАВИТЬ РЕАКЦИЮ НА СООБЩЕНИЕ АВТОРА [true=✅, false=❌]

            # channelSend = None, # ОТПРАВИТЬ СООБЩЕНИЕ В КАНАЛ [id канала]
            # MemberSend = None, # ОТПРАВИТЬ СООБЩЕНИЕ В ЛС [текст сообщения]
            # MemberDelete = None, # УДАЛИТЬ ЧЕРЕЗ [время в секундах]

            # customCommand = None,
            # cycleFieldEval = None, # техническая: только для команды `help`
            cycleFieldName = inf, # кортеж ['', '']
            cycleFieldValue = time, # кортеж ['', '']

            self = self, ctx = ctx, member = None, # ТЕХНИЧЕСКИЕ КОММАНДЫ
            )








    @commands.command()
    async def gesadd( self, ctx, exp: int, *, desc ):

        cursor.execute(f"INSERT INTO gesway_action (id, datetime, action, xp) VALUES ({ctx.author.id}, CURTIME(), '{desc}', {exp})")
        cursor.execute(f"UPDATE gesway SET xp = xp + {exp} WHERE id = {ctx.author.id}") #проверка, существует ли участник в БД
        connection.commit()

        await ctx.send(f'Готово нахуй. Ты выполнил: `{desc}` и за это тебе дали `{exp} опыта` :D')




    @commands.command()
    async def geshelp( self, ctx ):

        name = [f'{var.PREFIX}geshelp', f'{var.PREFIX}gesreg', f'{var.PREFIX}gesadd `[кол-во опыта]` `[достижение]`', f'{var.PREFIX}gesday `(день)` `(месяц)` `(год)`', f'{var.PREFIX}gesremove `[номер по списку]`', f'{var.PREFIX}gestop `(день/неделя/месяц/год)`', f'{var.PREFIX}gesuser', f'{var.PREFIX}gesrank', f'{var.PREFIX}geslist (дни/недели/месяца/года)']
        value = ['Вызвать это меню', 'Регистрация в Gesway', 'Добавить достижение', 'Посмотреть список достижений', 'Удалить запись *(в разработке)*', 'Список лидеров *(в разработке)*', 'Аналитика своего профиля *(в разработке)*', 'Информация про систему уровней *(в разработке)*', 'Запросить список своих результатов']

        await embed_func(
            desc = f"""
:heart: {ctx.author.mention} Добро пожаловать в крутую и уникальную систему опыта

:sparkles: Этот проект разработан не ради соревнования с другими — не нужно врать самому же себе

:white_check_mark: Сделал дело - Оценил сколько можно получить за это опыта - Готово

:bar_chart: Получай статистику и анализируй свою продуктивность вместе с проектом Gesway :D

*Что значат скобки?*
`[] - обязательное поле`
`() - необязательное поле`

**Gesway: Список всех команд**
            """, #ОСНОВНАЯ ИНФОРМАЦИЯ
            col = var.gesColorHelp, # ЦВЕТ EMBED
            # title = None, # ЗАГОЛОВОК
            authorMsg = True, # ОТОБРАЗИТЬ АВТОРА, КОТОРЫЙ ВЫЗВАЛ КОМАНДУ
            # field_name = None, field_value = None, # ИМЯ И ЗНАЧЕНИЕ
            img_url = 'https://phonoteka.org/uploads/posts/2021-06/1624880314_24-phonoteka_org-p-oboi-na-rabochii-stol-kosmos-fioletovii-kr-25.jpg', # КАРТИНКА
            footer_text = var.gesFooter, # FOOTER ТЕКСТ

            # deleteMsg = False, # УДАЛИТЬ СООБЩЕНИЕ АВТОРА
            deleteBtn = True, # УДАЛЕНИЕ СООБЩЕНИЯ НАЖАВ НА РЕАКЦИЮ
            deleteAuto = None, # АВТОМАТИЧЕСКОЕ УДАЛЕНИЕ ЧЕРЕЗ [время в секундах]

            reactionMsg = True, # ДОБАВИТЬ РЕАКЦИЮ НА СООБЩЕНИЕ АВТОРА [true=✅, false=❌]

            # channelSend = None, # ОТПРАВИТЬ СООБЩЕНИЕ В КАНАЛ [id канала]
            # MemberSend = None, # ОТПРАВИТЬ СООБЩЕНИЕ В ЛС [текст сообщения]
            # MemberDelete = None, # УДАЛИТЬ ЧЕРЕЗ [время в секундах]

            # customCommand = None,
            # cycleFieldEval = None, # техническая: только для команды `help`
            cycleFieldName = name, # кортеж ['', '']
            cycleFieldValue = value, # кортеж ['', '']

            self = self, ctx = ctx, member = None, # ТЕХНИЧЕСКИЕ КОММАНДЫ
            )



    @commands.command()
    async def gesuser( self, ctx ):

        #ОСНОВНАЯ СТАТИСТИКА
        select_sum_xp = 'SELECT SUM(xp) FROM gesway_action'
        cursor.execute(f"{select_sum_xp} WHERE id = {ctx.author.id} AND DATE(`datetime`) = CURDATE()")
        today_xp = cursor.fetchone()

        cursor.execute(f"{select_sum_xp} WHERE id = {ctx.author.id} AND DATE(`datetime`) = DATE(NOW() - INTERVAL 1 DAY)")
        yesterday_xp = cursor.fetchone()


        if today_xp[0] == None:
            today_xp = [0]

        if today_xp[0] > yesterday_xp[0]:
            today_yesterday_xp = today_xp[0] - yesterday_xp[0]
            how_many = f'**{today_yesterday_xp}exp** больше'
        elif today_xp[0] == yesterday_xp[0]:
            today_yesterday_xp = 0
            how_many = f'**{today_yesterday_xp}exp** *(одинаково)*'
        else:
            today_yesterday_xp = yesterday_xp[0] - today_xp[0]
            how_many = f'**{today_yesterday_xp}exp** меньше'


        #СРЕДНИЕ ПОКАЗАТЕЛИ ЗА ДЕНЬ
        select_avg_xp = 'SELECT ROUND(AVG(xp), 0) FROM gesway_action'
        cursor.execute(f"{select_avg_xp} WHERE id = {ctx.author.id}")
        day_avg_xp = cursor.fetchone()

        #ФУНКЦИЯ: СРЕДНИЕ ПОКАЗАТЕЛИ
        def avg_xp(group):
            cursor.execute(f'''SELECT ROUND(AVG(xp), 0)
FROM gesway_action
WHERE id = {ctx.author.id}
GROUP BY {group}''')
            result = cursor.fetchall()

            lis = []
            for i in result:
                for o in i:
                    lis.append(o)

            name = sum(lis)/len(lis)
            return round(name, 0)


        #ЛУЧШИЕ ПОКАЗАТЕЛИ: ДЕНЬ
        cursor.execute(f"SELECT MAX(xp), DAYOFMONTH(`datetime`), MONTH(`datetime`), YEAR(`datetime`) FROM gesway_action WHERE id = {ctx.author.id}")
        max_day_xp = cursor.fetchone()

        #ФУНКЦИЯ: ЛУЧШИЕ ПОКАЗАТЕЛИ
        def best_xp(group, sel):
            sel_month = f'SELECT SUM(xp) `xp`, DAYOFMONTH(`datetime`) day, MONTH(`datetime`) month, YEAR(`datetime`) year FROM gesway_action WHERE id = {ctx.author.id} GROUP BY {group}'
            sel_month_max = f'SELECT MAX(t.xp) FROM ( {sel_month} ) t'
            cursor.execute(f'SELECT xp, {sel} FROM ( {sel_month} ) t WHERE t.xp = ({sel_month_max})')
            max_month_xp = cursor.fetchone()
            return max_month_xp

        best_month_xp = best_xp('MONTH(`datetime`)', 'month, year')
        best_year_xp = best_xp('YEAR(`datetime`)', 'year')


        cursor.execute(f'SELECT SUM(xp) FROM gesway_action WHERE id = {ctx.author.id}')
        sum_xp = cursor.fetchone()[0]






        # ! ОСНОВА

        embed = discord.Embed( title = 'Gesway: Аналитика профиля', description = f'''
{ctx.author.mention} Спасибо тебе за то, что пользуешься Gesway :D

**:bar_chart: Основная статистика:**
За сегодня: **`[+{today_xp[0]}exp]`** _на {how_many}, чем вчера [{yesterday_xp[0]}exp]_
-За эту неделю: **`[+760exp]`** _на **260exp** меньше, чем на прошлой [500exp]_
-За этот месяц: **`[+1.650exp]`** _на **550exp** больше, чем за прошлый [1.100exp]_

**:tada: Твои средние показатели:**
За день: **`[{day_avg_xp[0]}exp]`**
За неделю: **`[{avg_xp( 'WEEK(datetime)')}exp]`**
За месяц: **`[{avg_xp( 'MONTH(datetime)')}exp]`**

**:trophy: Твоя лучшая продуктивность:**
Самый продуктивный день: `{max_day_xp[1]}.{max_day_xp[2]}.{max_day_xp[3]}` **`[+{max_day_xp[0]}exp]`**
Самый продуктивный месяц: `{best_month_xp[1]}.{best_month_xp[2]}` **`[+{best_month_xp[0]}exp]`**
Самый продуктивный год: `{best_year_xp[1]}` **`[+{best_year_xp[0]}exp]`**
⠀
        ''', color = var.gesColorMain )

        # embed.set_author( name = f'{ctx.message.author}', icon_url = ctx.message.author.avatar )

        embed.set_thumbnail (url = ctx.author.avatar)

        embed.add_field( name = ':crystal_ball: Уровень', value = '**`-1 LVL`** \n *(-всего 10 уровней)*', inline = True )
        embed.add_field( name = ':sparkles: Опыт', value = f'**`{sum_xp}exp`** из **`500exp`** \n *(осталось: 480exp)*', inline = True )
        embed.add_field( name = 'Дата регистрации', value = '`-01.12.2022` \n *(-ты с нами 6 дней)*', inline = True )


        embed.set_footer( text = var.gesFooter )

        await ctx.message.add_reaction("✅")
        await ctx.send( embed = embed )



    # @commands.command()
    # async def gesremove( self, ctx, number ):

    #     cursor.execute(f"INSERT INTO gesway_action (id, datetime, action, xp) VALUES ({ctx.author.id}, CURTIME(), '{desc}', {exp})")
    #     cursor.execute(f"UPDATE gesway SET xp = xp + {exp} WHERE id = {ctx.author.id}") #проверка, существует ли участник в БД
    #     connection.commit()

    #     await ctx.send(f'Готово нахуй. Ты удалил: `{desc}` и за это тебе дали `{exp} опыта` :D')



    @commands.command()
    async def geslist( self, ctx, day = None ):


        try:
            test = f'SELECT SUM(xp) `xp`, MONTH(`datetime`) month, YEAR(`datetime`) year FROM gesway_action WHERE id = {ctx.author.id} GROUP BY MONTH(`datetime`)'
            # sel_month_max = f'SELECT MAX(t.xp) FROM ( {sel_month} ) t'
            # cursor.execute(f'SELECT xp, {sel} FROM ( {sel_month} ) t WHERE t.xp = ({sel_month_max})')
            cursor.execute(f'{test}')
            result = cursor.fetchall()
            print(result)
        except Exception as e:
            print(f"error gesREG: {e}")


        # await embed_func(
        #     desc = None, #ОСНОВНАЯ ИНФОРМАЦИЯ
        #     col = var.cMain, # ЦВЕТ EMBED
        #     title = None, # ЗАГОЛОВОК
        #     authorMsg = False, # ОТОБРАЗИТЬ АВТОРА, КОТОРЫЙ ВЫЗВАЛ КОМАНДУ
        #     field_name = None, field_value = None, # ИМЯ И ЗНАЧЕНИЕ
        #     img_url = None, # КАРТИНКА
        #     footer_text = None, # FOOTER ТЕКСТ

        #     deleteMsg = False, # УДАЛИТЬ СООБЩЕНИЕ АВТОРА
        #     deleteBtn = False, # УДАЛЕНИЕ СООБЩЕНИЯ НАЖАВ НА РЕАКЦИЮ
        #     deleteAuto = None, # АВТОМАТИЧЕСКОЕ УДАЛЕНИЕ ЧЕРЕЗ [время в секундах]

        #     reactionMsg = None, # ДОБАВИТЬ РЕАКЦИЮ НА СООБЩЕНИЕ АВТОРА [true=✅, false=❌]

        #     channelSend = None, # ОТПРАВИТЬ СООБЩЕНИЕ В КАНАЛ [id канала]
        #     MemberSend = None, # ОТПРАВИТЬ СООБЩЕНИЕ В ЛС [текст сообщения]
        #     MemberDelete = None, # УДАЛИТЬ ЧЕРЕЗ [время в секундах]

        #     # customCommand = None,
        #     cycleFieldEval = None, # техническая: только для команды `help`
        #     cycleFieldName = None, # кортеж ['', '']
        #     cycleFieldValue = None, # кортеж ['', '']

        #     self = None, ctx = None, member = None, # ТЕХНИЧЕСКИЕ КОММАНДЫ
        #     )






async def setup(bot):
    await bot.add_cog(Gesway(bot))

print( 'Cogs - "Gesway" connected' )