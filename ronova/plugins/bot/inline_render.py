from pyrogram import Client, filters
from pyrogram.types import (InlineQuery, InlineQueryResultArticle, InputTextMessageContent,
                             InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery)

from config import ADMIN_ID
from ..utilities import GetServices, session


@Client.on_inline_query(filters.regex('render') & filters.user(ADMIN_ID))
async def inline_render(c: Client, q: InlineQuery):
    getter = GetServices()

    services = await getter.get_services(session)

    if not services:
        return await q.answer(
            results=[],
            switch_pm_text="No active services found",
            switch_pm_parameter="start"
        )

    results = []
    for svc in services:
        results.append(
            InlineQueryResultArticle(
                title=svc["name"],
                description=f'Region: {svc["region"]} • Branch: {svc["branch"]}',
                input_message_content=InputTextMessageContent(
                    f'**Service:** `{svc["name"]}`\n'
                    f'**ID:** `{svc["id"]}`\n'
                    f'**Type:** `{svc["type"]}`\n'
                    f'**Region:** `{svc["region"]}`\n'
                    f'**Branch:** `{svc["branch"]}`\n'
                    f'**URL:** {svc["url"]}'
                ),
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("🔁 Redeploy", callback_data=f'redeploy_{svc["id"]}')]]
                )
            )
        )

    await q.answer(results=results, cache_time=0)


@Client.on_callback_query(filters.regex(r'^redeploy_'))
async def redeploy_callback(c: Client, cb: CallbackQuery):

    if cb.from_user.id not in ADMIN_ID:
        return await cb.answer("Not allowed", show_alert=True)
    
    service_id = cb.data.split('_', 1)[1]
    getter = GetServices()

    await cb.answer("Triggering redeploy...", show_alert=False)

    deploy_id = await getter.trigger_deploy(session, service_id)

    if deploy_id:
        new_text = cb.message.text + f'\n\n**Redeploy triggered:** `{deploy_id}`'
        await c.edit_inline_text(
            cb.inline_message_id, 
            new_text
            )
    else:
        await cb.answer("Redeploy failed. Check API key/service ID.", show_alert=True)