import time

from pyrogram import Client, filters
from pyrogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
)

from ..utilities import eval_helper
from config import ADMIN_ID


@Client.on_inline_query(filters.regex("ping") & filters.user(ADMIN_ID))
async def inline_ping(c: Client, q: InlineQuery):
    print("T_T will be added")