from pyrogram import idle
import uvloop

from ronova import ub, bot
from .server import startServer

async def close_session():
    from .plugins.utilities import session
    await session.close()

async def main():
    try:
        await bot.start()
        await ub.start()

        asyncio.create_task(startServer())

        print("Bot and UB started!")

        await idle()
    finally:
        await ub.stop()
        await bot.stop()
        await close_session()

uvloop.install()
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())