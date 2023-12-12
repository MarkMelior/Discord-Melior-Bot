from config import PREFIX

# ? ALIASES: /КОМАНДА
aClear = [ 'clear', 'очистить', 'del' ]
aReport = [ 'report', 'репорт' ]
aStatusPlaying = [ 'plays', 'играть' ]
aStatusWatch = [ 'watch', 'смотреть' ]
aStatusListen = [ 'listen', 'слушать' ]
aStatusStream = [ 'stream', 'стрим' ]
aRandom = [ 'random', 'рандом' ]
aDuel = [ 'duel', 'дуэль' ]
aGift = [ 'gift', 'подарить', 'подарок', 'дать', 'дарить' ]
aChat = [ 'chat', 'чат', 'действие', f'{PREFIX}' ]
aWarn = [ 'warn', 'варн', 'предупредить' ]
aRename = [ 'rename' ]
aBan = [ 'ban', 'бан' ]

aMusicDownload = [ 'download', 'скачать' ]
aMusicVolume = [ 'volume', 'звук', 'vol' ]
aMusicJoin = [ 'join', 'подключить' ]
aMusicInfo = [ 'sound-inf', 'муз-инф' ]
aMusicQueue = [ 'queue', 'очередь' ]
aMusicResume = [ 'resume', 'возобновить' ]
aMusicPause = [ 'pause', 'пауза' ]
aMusicLeave = [ 'leave', 'отключить' ]
aMusicStop = [ 'stop', 'остановить' ]
aMusicSkip = [ 'skip', 'пропустить' ]
aMusicReset = [ 'reset', 'перезапустить' ]
aMusicRepeat = [ 'repeat', 'повторить' ]
aMusicPlay = [ 'play', 'музыка' ]

aHelp = [ 'help', 'помощь', 'хелп', 'помоги' ]
aHelpModer = [ 'moder', 'модер', 'модерация', 'модерации' ]
aHelpChat = [ 'chat', 'action', 'чат', 'по чату', 'по действиям', 'с чатом', 'действия' ]
aHelpOther = [ 'other', 'другое' ]
aHelpGame = [ 'game' ]
aHelpDev = [ 'dev', 'разраб', 'developer', 'разработчик' ]
aHelpMusic = [ 'music', 'музыка', 'муз', 'по музыке', 'mus' ]

aGameBalance = [ 'balance', 'баланс', 'cash' ]
aGamePay = [ 'pay', 'givecash', 'перевести' ]
aGameBonus = [ 'bonus', 'бонус' ]
aGameAward = [ 'award', 'зачислить' ]
aGameTake = [ 'take', 'снять' ]
aGameCasino = [ 'casino', 'казино' ]
aGameStats = [ 'user', 'стат', 'профиль', 'prof', 'profile', 'проф', 'статистика' ]
aGameTop = [ 'top', 'топ' ]
aGameRoulette = ['roulette', 'рулетка', 'ставка']
aGameWork = [ 'work', 'работа', 'работать' ]

aShopAdd = ['addrole', 'addshop', 'role']
aShopRemove = ['delrole']
aShop = ['shop', 'магазин', 'магаз']
aShopBuy = ['buyrole']
aShopSell = ['sellrole']

# aUserProfile = [ 'profile', 'проф', 'профиль', 'prof', 'user' ]
# aUserLevel = [ 'level', 'уровень', 'lvl' ]

aLoad = [ 'load' ]
aUnload = [ 'unload' ]
aCogsList = [ 'cogslist' ]
aAllSend = [ 'allsend' ]
aUserSend = [ 'usersend' ] # отправить сообщение пользователям
aRoleSend = [ 'rolesend' ]
aRoulette = [ 'dead', 'вылет' ]

# ? BRIEF: ЗНАЧЕНИЕ КОМАНДЫ
bWarn = "Предупреждение"
bReport = "Отправить сообщение модерации"
bRandom = "Выбрать любое число"
bGift = "Отправить подарок"
bDuel = "Вызвать на дуэль. *Участника 2, Победитель 1*"
bClear = "Очистить чат"
bChat = "Выполнение действия в чате"
bBan = "Временная блокировка"
bLoad = "Подключить Cogs"
bUnload = "Отключить Cogs"
bCogsList = "Список всех доспутных когов"
bAllSend = "Отправить всем сообщение от имени бота"
bUserSend = "Отправить пользователю сообщение от имени бота"
bRoleSend = "Отправить пользователям (с указанной ролью) сообщение от имени бота"
bRoulette = "Рулетка на вылет из голосового чата"

bGameBalance = 'Посмотреть баланс пользователя'
bGamePay = 'Перевести деньги пользователю'
bGameBonus = 'Получить бонус'
bGameAward = "Зачислить указанную сумму пользователю"
bGameTake = "Снять указанную сумму у пользователя"
bGameCasino = "Сделать ставку в казино"
bGameStats = "Посмотреть статистику пользователя"
bGameTop = "Топ пользователей сервера"
bGameRoulette = 'Сделать ставку в рулетке'
bGameWork = "Заработать денег"

bShopAdd = 'Добавить роль в магазин'
bShopRemove = 'Удалить роль из магазина'
bShop = 'Магазин ролей'
bShopBuy = "Приобрести роль"
bShopSell = "Продать роль за пол цены"

bUserProfile = "Статистика пользователя"
bUserLevel = 'Уровень пользователя'

bMusicDownload = 'Скачать музыку по ссылке'
bMusicVolume = "Изменить громкость звука"
bMusicJoin = "Подключить"
bMusicInfo = "Информация о музыке"
bMusicQueue = "Добавить музыку в очередь"
bMusicResume = "Возобновить музыку"
bMusicPause = "Поставить музыку на паузу"
bMusicLeave = "Отключить музыку"
bMusicStop = "Остановить музыку"
bMusicSkip = "Пропустить музыку"
bMusicReset = "Перезапустить музыку"
bMusicRepeat = "Повторить музыку"
bMusicPlay = "Включить музыку"

# ? USAGE: КАК ПРАВИЛЬНО ИСПОЛЬЗОВАТЬ КОМАНДУ
uWarn = f"{PREFIX}{aWarn[0]} ``[@user] [причина]``"
uReport = f"{PREFIX}{aReport[0]} ``[текст]``"
uRandom = f"{PREFIX}{aRandom[0]} ``[число]``"
uGift = f"{PREFIX}{aGift[0]} ``[emoji] [@user] (текст)``"
uDuel = f"{PREFIX}{aDuel[0]} ``[@user]``"
uClear = f"{PREFIX}{aClear[0]} ``[кол-во предложений]``"
uBan = f"{PREFIX}{aBan[0]} ``[@user] [время в минутах] [причина]``"
uChat = f"{PREFIX}{aChat[0]} ``[действие] [@user] (текст)``"
uChatSecond = "``[@user] (текст)``"
uLoad = f"{PREFIX}{aLoad[0]} ``[name cog]``"
uUnload = f"{PREFIX}{aUnload[0]} ``[name cog]``"
uCogsList = f"{PREFIX}{aCogsList[0]}"
uHelp = f"{PREFIX}{aHelp[0]} ``[{aHelpOther[0]}, {aHelpGame[0]}, {aHelpModer[0]}, {aHelpChat[0]}]``"
uAllSend = f"{PREFIX}{aAllSend[0]} ``[сообщение]``"
uUserSend = f"{PREFIX}{aUserSend[0]} ``[@user] [сообщение]``"
uRoleSend = f"{PREFIX}{aRoleSend[0]} ``[@role] [сообщение]``"
uRoulette = f"{PREFIX}{aRoulette[1]}"

uGameBalance = f"{PREFIX}{aGameBalance[0]} `(@user)`"
uGamePay = f"{PREFIX}{aGamePay[0]} `[@user] [сумма]`"
uGameBonus = f"{PREFIX}{aGameBonus[0]}"
uGameAward = f"[ADMIN] {PREFIX}{aGameAward[0]} `[@user]`"
uGameTake = f"[ADMIN] {PREFIX}{aGameTake[0]} `[@user]`"
uGameCasino = f"{PREFIX}{aGameCasino[0]} `[сумма]`"
uGameStats = f"{PREFIX}{aGameStats[0]} `(@user)`"
uGameTop = f"{PREFIX}{aGameTop[0]} `(xp)` or `(cash)`"
uGameRoulette = f"{PREFIX}{aGameRoulette[0]} `[сумма]` `[ставка]`"
uGameWork = f"{PREFIX}{aGameWork[0]} `[работа]`"

uShopAdd = f"[ADMIN] {PREFIX}{aShopAdd[0]} `[@role]` `[cost]`"
uShopRemove = f"[ADMIN] {PREFIX}{aShopRemove[0]} `[@role]`"
uShop = f"{PREFIX}{aShop[0]}"
uShopBuy = f"{PREFIX}{aShopBuy[0]} `[@role]`"
uShopSell = f"{PREFIX}{aShopSell[0]} `[@role]`"

# uUserProfile = f"{PREFIX}{aUserProfile[0]} ``(@user)``"
# uUserLevel = f"{PREFIX}{aUserLevel[0]} ``(@user)``"

uMusicDownload = f"{PREFIX}{aMusicDownload[0]} ``[ссылка]``"
uMusicVolume = f"{PREFIX}{aMusicVolume[0]} ``[громкость 0/200]``"
uMusicJoin = f"{PREFIX}{aMusicJoin[0]} ``(канал)``"
uMusicInfo = f"{PREFIX}{aMusicInfo[0]}"
uMusicQueue = f"{PREFIX}{aMusicQueue[0]}"
uMusicResume = f"{PREFIX}{aMusicResume[0]}"
uMusicPause = f"{PREFIX}{aMusicPause[0]}"
uMusicLeave = f"{PREFIX}{aMusicLeave[0]}"
uMusicStop = f"{PREFIX}{aMusicStop[0]}"
uMusicSkip = f"{PREFIX}{aMusicSkip[0]}"
uMusicReset = f"{PREFIX}{aMusicReset[0]}"
uMusicRepeat = f"{PREFIX}{aMusicRepeat[0]}"
uMusicPlay = f"{PREFIX}{aMusicPlay[0]} ``[ссылка]``"