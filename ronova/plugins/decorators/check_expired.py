from functools import wraps

from pyrogram import Client
from pyrogram.errors import FileReferenceExpired

from ..shared import AFK_DATA
from ..utilities import extract_media

def on_expired(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)

        except FileReferenceExpired:

            c:Client = args[0]

            msg = await c.get_messages(
                AFK_DATA.media_from_chat,
                AFK_DATA.message_media_id
            )

            AFK_DATA.file_id, AFK_DATA.file_type = extract_media(msg)

            return await func(*args, **kwargs)

    return wrapper