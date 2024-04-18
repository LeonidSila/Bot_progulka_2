from create_bot import dp, bot
import asyncio
from database import data_base
from client import client_main as cl

data_base.creat_teble()


dp.include_router(cl.router_client)


async def start():
    try:
        await dp.start_polling(bot)
    except:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())
