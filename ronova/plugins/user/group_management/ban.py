from datetime import datetime, timezone
from typing import Optional

from pyrogram import Client, filters
from pyrogram.types import Message

from config import PREFIXES, ADMIN_ID
from .utils import RetriveData, format_duration

COMMAND_BANS: list[str] = ["ban", "dban", "cban", "sban"]


async def ban_user(
    c: Client,
    m: Message,
    chat_id: int,
    target_id: int,
    time: Optional[datetime],
    revoke_messages: bool = False,
    revoke_reactions: bool = False,
):  
    try:
        await c.ban_chat_member(
            chat_id=chat_id,
            user_id=target_id,
            until_date=time,
            revoke_messages=revoke_messages,
            revoke_reactions=revoke_reactions,
        )
        return True

    except Exception as e:
        await m.reply_text(f"Ban failed:\n{e}")
        return False


@Client.on_message(
    filters.command(COMMAND_BANS, prefixes=PREFIXES)
    & filters.user(ADMIN_ID)
    & filters.group
)
async def gc_mang(c: Client, m: Message):

    parser = RetriveData(c, m)
    
    data = await parser.ban_data()

    chat_id = data["chat_id"]
    target_id = data["target_id"]
    time = data["time"]
    reason = data["reason"]

    if not target_id or target_id == m.from_user.id:
        return

    cmd = m.command[0]
    duration = format_duration(time)

    text = f"Banned user `{target_id}` for {duration}"
    if reason:
        text += f"\nReason: {reason}"

    if cmd == "ban":
        if await ban_user(c, m, chat_id, target_id, time):
            await m.reply_text(text)

    elif cmd == "dban":
        if m.reply_to_message:
            await m.reply_to_message.delete()

        if await ban_user(c, m, chat_id, target_id, time):
            await m.reply_text(text)

    elif cmd == "sban":
        if await ban_user(c, chat_id, target_id, time):
            await m.delete()

    elif cmd == "cban":
        await ban_user(
            c,
            m,
            chat_id,
            target_id,
            time,
            revoke_messages=True,
            revoke_reactions=True,
        )
        if await ban_user(c, m, chat_id, target_id, time):
            await m.reply_text(text)
