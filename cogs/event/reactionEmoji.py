from nextcord.ext import commands
import random


class reactionEmoji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # РЕАКЦИЯ БОТА НА ЭМОДЗИКИ
    @commands.Cog.listener()
    async def on_message( self, message ):
        msg = message.content.lower()
        TableEmoji = [ '😀', '😃', '😄', '😁', '😆', '😅', '😂', '🤣', '😇', '😉', '😊', '🙂', '🙃', '☺', '😋', '😌', '😍', '🥰', '😘', '😗', '😙', '😚', '🤪', '😜', '😝', '😛', '🤑', '😎', '🤓', '🧐', '🤠', '🥳', '🤗', '🤡', '😏', '😶', '😐', '😑', '😒', '🙄', '🤨', '🤔', '🤫', '🤭', '🤥', '😳', '😞', '😟', '😠', '😡', '🤬', '😔', '😕', '🙁', '☹', '😬', '🥺', '😣', '😖', '😫', '😩', '🥱', '😤', '😮', '😱', '😨', '😰', '😯', '😦', '😧', '😢', '😥', '😪', '🤤', '😓', '😭', '🤩', '😵', '🥴', '😲', '🤯', '🤐', '😷', '🤕', '🤒', '🤮', '🤢', '🤧', '🥵', '🥶', '😴', '💤', '😈', '👿', '👹', '👺', '💩', '👻', '💀', '☠', '👽', '🤖', '🎃', '😺', '😸', '😹', '😻', '😼', '😽', '🙀', '😿', '😾', '👐', '🤲', '🙌', '👏', '🙏', '🤝', '👍', '👎', '👊', '✊', '🤛', '🤜', '🤞', '✌', '🤘', '🤟', '👌', '🤏', '👈', '👉', '👆', '👇', '☝', '✋', '🤚', '🖐', '🖖', '👋', '🤙', '💪', '🦾', '🖕', '✍', '🤳', '💅', '🦵', '🦿', '🦶', '👄', '🦷', '👅', '👂', '🦻', '👃', '👁', '👀', '🧠', '🦴', '👤', '👥', '🗣', '👶', '👧', '🧒', '👦', '👩', '🧑', '👨', '👩‍🦱', '🧑‍🦱', '👨‍🦱', '👩‍🦰', '🧑‍🦰', '👨‍🦰', '👱‍♀️', '👱', '👱‍♂️', '👩‍🦳', '🧑‍🦳', '👨‍🦳', '👩‍🦲', '🧑‍🦲', '👨‍🦲', '🧔', '👵', '🧓', '👴', '👲', '👳‍♀️', '👳', '👳‍♂️', '🧕', '👼', '👸', '🤴', '👰', '🤵‍♀️', '🤵', '🤵‍♂️', '🙇‍♀️', '🙇', '🙇‍♂️', '💁‍♀️', '💁', '💁‍♂️', '🙅‍♀️', '🙅', '🙅‍♂️', '🙆‍♀️', '🙆', '🙆‍♂️', '🤷‍♀️', '🤷', '🤷‍♂️', '🙋‍♀️', '🙋', '🙋‍♂️', '🤦‍♀️', '🤦', '🤦‍♂️', '🧏‍♀️', '🧏', '🧏‍♂️', '🙎‍♀️', '🙎', '🙎‍♂️', '🙍‍♀️', '🙍', '🙍‍♂️', '💇‍♀️', '💇', '💇‍♂️', '💆‍♀️', '💆', '💆‍♂️', '🤰', '🤱', '🧎‍♀️', '🧎', '🧎‍♂️', '🧍‍♀️', '🧍', '🧍‍♂️', '🚶‍♀️', '🚶', '🚶‍♂️', '👩‍🦯', '🧑‍🦯', '👨‍🦯', '🏃‍♀️', '🏃', '🏃‍♂️', '👩‍🦼', '🧑‍🦼', '👨‍🦼', '👩‍🦽', '🧑‍🦽', '👨‍🦽', '💃', '🕺', '👫', '🧑‍🤝‍🧑', '👩‍❤️‍👨', '💑', '👩‍❤️‍💋‍👨', '💏', '❤', '🧡', '💛', '💚', '💙', '💜', '🤎', '🖤', '🤍', '💔', '❣', '💕', '💞', '💓', '💗', '💖', '💘', '💝', '💟'
            '🍏', '🍎', '🍐', '🍊', '🍋', '🍌', '🍉', '🍇', '🍓', '🍈', '🍒', '🍑', '🥭', '🍍', '🥥', '🥝', '🍅', '🥑', '🍆', '🌶', '🥒', '🥬', '🥦', '🧄', '🧅', '🌽', '🥕', '🥗', '🥔', '🍠', '🥜', '🍯', '🍞', '🥐', '🥖', '🥨', '🥯', '🥞', '🧇', '🧀', '🍗', '🍖', '🥩', '🍤', '🥚', '🍳', '🥓', '🍔', '🍟', '🌭', '🍕', '🍝', '🥪', '🌮', '🌯', '🥙', '🧆', '🍜', '🥘', '🍲', '🥫', '🧂', '🧈', '🍥', '🍣', '🍱', '🍛', '🍙', '🍚', '🍘', '🥟', '🍢', '🍡', '🍧', '🍨', '🍦', '🍰', '🎂', '🧁', '🥧', '🍮', '🍭', '🍬', '🍫', '🍿', '🍩', '🍪', '🥠', '🥮', '☕', '🍵', '🥣', '🍼', '🥤', '🧃', '🧉', '🥛', '🍺', '🍻', '🍷', '🥂', '🥃', '🍸', '🍹', '🍾', '🍶', '🧊', '🥄', '🍴', '🍽', '🥢', '🥡'
            '⚽', '🏀', '🏈', '⚾', '🥎', '🎾', '🏐', '🏉', '🎱', '🥏', '🏓', '🏸', '🥅', '🏒', '🏑', '🏏', '🥍', '🥌', '⛳', '🏹', '🎣', '🤿', '🥊', '🥋', '⛸', '🎿', '🛷', '⛷', '🏂', '🏋️‍♀️', '🏋', '🏋️‍♂️', '🤺', '🤼‍♀️', '🤼', '🤼‍♂️', '🤸‍♀️', '🤸', '🤸‍♂️', '⛹️‍♀️', '⛹', '⛹️‍♂️', '🤾‍♀️', '🤾', '🤾‍♂️', '🧗‍♀️', '🧗', '🧗‍♂️', '🏌️‍♀️', '🏌', '🏌️‍♂️', '🧘‍♀️', '🧘', '🧘‍♂️', '🧖‍♀️', '🧖', '🧖‍♂️', '🏄‍♀️', '🏄', '🏄‍♂️', '🏊‍♀️', '🏊', '🏊‍♂️', '🤽‍♀️', '🤽', '🤽‍♂️', '🚣‍♀️', '🚣', '🚣‍♂️', '🏇', '🚴‍♀️', '🚴', '🚴‍♂️', '🚵‍♀️', '🚵', '🚵‍♂️', '🎽', '🎖', '🏅', '🥇', '🥈', '🥉', '🏆', '🏵', '🎗', '🎫', '🎟', '🎪', '🤹‍♀️', '🤹', '🤹‍♂️', '🎭', '🎨', '🎬', '🎤', '🎧', '🎼', '🎹', '🥁', '🎷', '🎺', '🎸', '🪕', '🎻', '🎲', '🧩', '♟', '🎯', '🎳', '🪀', '🪁', '🎮', '👾', '🎰', '👮‍♀️', '👮', '👮‍♂️', '👩‍🚒', '🧑‍🚒', '👨‍🚒', '👷‍♀️', '👷', '👷‍♂️', '👩‍🏭', '🧑‍🏭', '👨‍🏭', '👩‍🔧', '🧑‍🔧', '👨‍🔧', '👩‍🌾', '🧑‍🌾', '👨‍🌾', '👩‍🍳', '🧑‍🍳', '👨‍🍳', '👩‍🎤', '🧑‍🎤', '👨‍🎤', '👩‍🎨', '🧑‍🎨', '👨‍🎨', '👩‍🏫', '🧑‍🏫', '👨‍🏫', '👩‍🎓', '🧑‍🎓', '👨‍🎓', '👩‍💼', '🧑‍💼', '👨‍💼', '👩‍💻', '🧑‍💻', '👨‍💻', '👩‍🔬', '🧑‍🔬', '👨‍🔬', '👩‍🚀', '🧑‍🚀', '👨‍🚀', '👩‍⚕️', '🧑‍⚕️', '👨‍⚕️', '👩‍⚖️', '🧑‍⚖️', '👨‍⚖️', '👩‍✈️', '🧑‍✈️', '👨‍✈️', '💂‍♀️', '💂', '💂‍♂️', '🕵️‍♀️', '🕵', '🕵️‍♂️', '🤶', '🎅', '🕴️‍♀️', '🕴', '🕴️‍♂️', '🦸‍♀️', '🦸', '🦸‍♂️', '🦹‍♀️', '🦹', '🦹‍♂️', '🧙‍♀️', '🧙', '🧙‍♂️', '🧝‍♀️', '🧝', '🧝‍♂️', '🧚‍♀️', '🧚', '🧚‍♂️', '🧞‍♀️', '🧞', '🧞‍♂️', '🧜‍♀️', '🧜', '🧜‍♂️', '🧛‍♀️', '🧛', '🧛‍♂️', '🧟‍♀️', '🧟', '🧟‍♂️', '👯‍♀️', '👯', '👯‍♂️', '👪', '👨‍👩‍👧', '👨‍👩‍👧‍👦', '👨‍👩‍👦‍👦', '👨‍👩‍👧‍👧', '👩‍👦', '👩‍👧', '👩‍👧‍👦', '👩‍👦‍👦', '👩‍👧‍👧', '👨‍👦', '👨‍👧', '👨‍👧‍👦', '👨‍👦‍👦', '👨‍👧‍👧'
            '🚗', '🚙', '🚕', '🛺', '🚌', '🚎', '🏎', '🚓', '🚑', '🚒', '🚐', '🚚', '🚛', '🚜', '🏍', '🛵', '🚲', '🦼', '🦽', '🛴', '🛹', '🚨', '🚔', '🚍', '🚘', '🚖', '🚡', '🚠', '🚟', '🚃', '🚋', '🚝', '🚄', '🚅', '🚈', '🚞', '🚂', '🚆', '🚇', '🚊', '🚉', '🚁', '🛩', '✈', '🛫', '🛬', '🪂', '💺', '🛰', '🚀', '🛸', '🛶', '⛵', '🛥', '🚤', '⛴', '🛳', '🚢', '⚓', '⛽', '🚧', '🚏', '🚦', '🚥', '🛑', '🎡', '🎢', '🎠', '🏗', '🌁', '🗼', '🏭', '⛲', '🎑', '⛰', '🏔', '🗻', '🌋', '🗾', '🏕', '⛺', '🏞', '🛣', '🛤', '🌅', '🌄', '🏜', '🏖', '🏝', '🌇', '🌆', '🏙', '🌃', '🌉', '🌌', '🌠', '🎇', '🎆', '🏘', '🏰', '🏯', '🏟', '🗽', '🏠', '🏡', '🏚', '🏢', '🏬', '🏣', '🏤', '🏥', '🏦', '🏨', '🏪', '🏫', '🏩', '💒', '🏛', '⛪', '🕌', '🛕', '🕍', '🕋', '⛩'
            '⌚', '📱', '📲', '💻', '⌨', '🖥', '🖨', '🖱', '🖲', '🕹', '🗜', '💽', '💾', '💿', '📀', '📼', '📷', '📸', '📹', '🎥', '📽', '🎞', '📞', '☎', '📟', '📠', '📺', '📻', '🎙', '🎚', '🎛', '⏱', '⏲', '⏰', '🕰', '⏳', '⌛', '🧮', '📡', '🔋', '🔌', '💡', '🔦', '🕯', '🧯', '🗑', '🛢', '🛒', '💸', '💵', '💴', '💶', '💷', '💰', '💳', '🧾', '💎', '⚖', '🦯', '🧰', '🔧', '🔨', '⚒', '🛠', '⛏', '🪓', '🔩', '⚙', '⛓', '🧱', '🔫', '🧨', '💣', '🔪', '🗡', '⚔', '🛡', '🚬', '⚰', '⚱', '🏺', '🔮', '📿', '🧿', '💈', '🧲', '⚗', '🧪', '🧫', '🧬', '🔭', '🔬', '🕳', '💊', '💉', '🩸', '🩹', '🩺', '🌡', '🏷', '🔖', '🚽', '🚿', '🛁', '🛀', '🪒', '🧴', '🧻', '🧼', '🧽', '🧹', '🧺', '🔑', '🗝', '🛋', '🪑', '🛌', '🛏', '🚪', '🧳', '🛎', '🖼', '🧭', '🗺', '⛱', '🗿', '🛍', '🎈', '🎏', '🎀', '🧧', '🎁', '🎊', '🎉', '🎎', '🎐', '🏮', '🪔', '✉', '📩', '📨', '📧', '💌', '📮', '📪', '📫', '📬', '📭', '📦', '📯', '📥', '📤', '📜', '📃', '📑', '📊', '📈', '📉', '📄', '📅', '📆', '🗓', '📇', '🗃', '🗳', '🗄', '📋', '🗒', '📁', '📂', '🗂', '🗞', '📰', '📓', '📕', '📗', '📘', '📙', '📔', '📒', '📚', '📖', '🔗', '📎', '🖇', '✂', '📐', '📏', '📌', '📍', '🧷', '🧵', '🧶', '🔐', '🔒', '🔓', '🔏', '🖊', '🖋', '✒', '📝', '✏', '🖍', '🖌', '🔍', '🔎', '👚', '👕', '🥼', '🦺', '🧥', '👖', '👔', '👗', '👘', '🥻', '🩱', '👙', '🩲', '🩳', '💄', '💋', '👣', '🧦', '👠', '👡', '👢', '🥿', '👞', '👟', '🩰', '🥾', '🧢', '👒', '🎩', '🎓', '👑', '⛑', '🎒', '👝', '👛', '👜', '💼', '👓', '🕶', '🥽', '🧣', '🧤', '💍', '🌂', '☂'
            '☮', '✝', '☪', '🕉', '☸', '✡', '🔯', '🕎', '☯', '☦', '🛐', '⛎', '♈', '♉', '♊', '♋', '♌', '♍', '♎', '♏', '♐', '♑', '♒', '♓', '🆔', '⚛', '⚕', '☢', '☣', '📴', '📳', '🈶', '🈚', '🈸', '🈺', '🈷', '✴', '🆚', '🉑', '💮', '🉐', '㊙', '㊗', '🈴', '🈵', '🈹', '🈲', '🅰', '🅱', '🆎', '🆑', '🅾', '🆘', '⛔', '📛', '🚫', '❌', '⭕', '💢', '♨', '🚷', '🚯', '🚳', '🚱', '🔞', '📵', '🚭', '❗', '❕', '❓', '❔', '‼', '⁉', '💯', '🔅', '🔆', '🔱', '⚜', '〽', '⚠', '🚸', '🔰', '♻', '🈯', '💹', '❇', '✳', '❎', '✅', '💠', '🌀', '➿', '🌐', '♾', 'Ⓜ', '🏧', '🚾', '♿', '🅿', '🈳', '🈂', '🛂', '🛃', '🛄', '🛅', '🚰', '🚹', '♂', '🚺', '♀', '⚧', '🚼', '🚻', '🚮', '🎦', '📶', '🈁', '🆖', '🆗', '🆙', '🆒', '🆕', '🆓', '0⃣', '1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟', '🔢', '▶', '⏸', '⏯', '⏹', '⏺', '⏏', '⏭', '⏮', '⏩', '⏪', '🔀', '🔁', '🔂', '◀', '🔼', '🔽', '⏫', '⏬', '➡', '⬅', '⬆', '⬇', '↗', '↘', '↙', '↖', '↕', '↔', '🔄', '↪', '↩', '🔃', '⤴', '⤵', '#⃣', '*⃣', 'ℹ', '🔤', '🔡', '🔠', '🔣', '🎵', '🎶', '〰', '➰', '✔', '➕', '➖', '➗', '✖', '💲', '💱', '©', '®', '™', '🔚', '🔙', '🔛', '🔝', '🔜', '☑', '🔘', '🔴', '🟠', '🟡', '🟢', '🔵', '🟣', '🟤', '⚫', '⚪', '🟥', '🟧', '🟨', '🟩', '🟦', '🟪', '🟫', '⬛', '⬜', '◼', '◻', '◾', '◽', '▪', '▫', '🔸', '🔹', '🔶', '🔷', '🔺', '🔻', '🔲', '🔳', '🔈', '🔉', '🔊', '🔇', '📣', '📢', '🔔', '🔕', '🃏', '🀄', '♠', '♣', '♥', '♦', '🎴', '👁‍🗨', '🗨', '💭', '🗯', '💬', '🕐', '🕑', '🕒', '🕓', '🕔', '🕕', '🕖', '🕗', '🕘', '🕙', '🕚', '🕛', '🕜', '🕝', '🕞', '🕟', '🕠', '🕡', '🕢', '🕣', '🕤', '🕥', '🕦', '🕧'
            '🐶', '🐱', '🐭', '🐹', '🐰', '🐻', '🧸', '🐼', '🐨', '🐯', '🦁', '🐮', '🐷', '🐽', '🐸', '🐵', '🙈', '🙉', '🙊', '🐒', '🦍', '🦧', '🐔', '🐧', '🐦', '🐤', '🐣', '🐥', '🐺', '🦊', '🦝', '🐗', '🐴', '🦓', '🦒', '🦌', '🦘', '🦥', '🦦', '🦄', '🐝', '🐛', '🦋', '🐌', '🐞', '🐜', '🦗', '🕷', '🕸', '🦂', '🦟', '🦠', '🐢', '🐍', '🦎', '🐙', '🦑', '🦞', '🦀', '🦐', '🦪', '🐠', '🐟', '🐡', '🐬', '🦈', '🐳', '🐋', '🐊', '🐆', '🐅', '🐃', '🐂', '🐄', '🐪', '🐫', '🦙', '🐘', '🦏', '🦛', '🐐', '🐏', '🐑', '🐎', '🐖', '🦇', '🐓', '🦃', '🕊', '🦅', '🦆', '🦢', '🦉', '🦩', '🦚', '🦜', '🐕', '🦮', '🐕‍🦺', '🐩', '🐈', '🐇', '🐀', '🐁', '🐿', '🦨', '🦡', '🦔', '🐾', '🐉', '🐲', '🦕', '🦖', '🌵', '🎄', '🌲', '🌳', '🌴', '🌱', '🌿', '☘', '🍀', '🎍', '🎋', '🍃', '🍂', '🍁', '🌾', '🌺', '🌻', '🌹', '🥀', '🌷', '🌼', '🌸', '💐', '🍄', '🌰', '🐚', '🌎', '🌍', '🌏', '🌕', '🌖', '🌗', '🌘', '🌑', '🌒', '🌓', '🌔', '🌙', '🌚', '🌝', '🌛', '🌜', '⭐', '🌟', '💫', '✨', '☄', '🪐', '🌞', '☀', '🌤', '⛅', '🌥', '🌦', '☁', '🌧', '⛈', '🌩', '⚡', '🔥', '💥', '❄', '🌨', '☃', '⛄', '🌬', '💨', '🌪', '🌫', '🌈', '☔', '💧', '💦', '🌊' ]
        TextEmoji = [ 'письколом', 'домашка по алгебре', 'заурбек', 'джигит', 'петрушка', 'овощь', 'доклад', 'стиралка', 'кот', 'осьминог', 'шоколадина', 'трусики', 'лифчик', 'баклажанище' ]

        dlina = len(TextEmoji) - 1
        l = list(range(0, dlina))
        random.shuffle(l)
        for i in l:
            pass

        if msg in TableEmoji:
            await message.channel.send( TextEmoji[i] )


def setup(bot):
    bot.add_cog(reactionEmoji(bot))

print( 'Cogs - "reactionEmoji" connected' )