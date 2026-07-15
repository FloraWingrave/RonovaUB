from pyrogram import Client, filters
from pyrogram.types import Message

from .errors import NoData

def starts(prefix: str | None = None):
    if prefix is None:
        raise NoData("pass a prefix in starts(prefix:str = '')")

    prefix = prefix.lower()

    async def func(flt, c: Client, m: Message):
        text = m.text
        if not text:
            return False

        return text.lower().startswith(prefix)

    return filters.create(func, name="StartsFilter")