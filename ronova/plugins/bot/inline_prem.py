import os

from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InlineQuery,
    InlineQueryResultArticle,
    CallbackQuery,
    InputTextMessageContent
)

from config import ADMIN_ID
from ..shared import PREMIUM_STATE
from ..premium.emoji_allies import emojis

def change_text(text: str):
    import re

    def replace_word(match):
        word = match.group(0)
        return emojis.get(word.lower(), word)

    text = re.sub(r"\b\w+\b", replace_word, text)

    for e, tg in emojis.items():
        text = text.replace(e, tg)

    return text

@Client.on_inline_query(filters.regex("prem (.+)") & filters.user(ADMIN_ID))
async def emo_in(c: Client, q: InlineQuery):

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("wait", callback_data="wait")]
    ])

    PREMIUM_STATE.text = change_text(q.matches[0].group(1))
    PREMIUM_STATE.status = True

    await q.answer([
        InlineQueryResultArticle(
            title="Premium Text",
            input_message_content=InputTextMessageContent(
                message_text="please wait...",
            ),
            reply_markup=keyboard
        )
    ])


@Client.on_callback_query(filters.regex("wait"))
async def clear_logs_cb(c: Client, cb: CallbackQuery):

    if cb.from_user.id not in ADMIN_ID:
        return await cb.answer("Not allowed", show_alert=True)

    await c.edit_inline_text(
        inline_message_id=cb.inline_message_id,
        text= PREMIUM_STATE.text
    )
    await cb.answer()
    PREMIUM_STATE.status = False
    PREMIUM_STATE.text = None