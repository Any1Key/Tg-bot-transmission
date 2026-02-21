from __future__ import annotations

import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.config import Settings, load_yaml_config
from bot.handlers import router
from bot.middlewares import AuthMiddleware, ThrottleMiddleware
from bot.services import DBService, Monitor, TransmissionService, make_session_factory
from bot.utils.logging import setup


async def main() -> None:
    s = Settings()
    y = load_yaml_config(s.config_path)
    setup(s.log_level)

    bot = Bot(token=s.token, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2))
    dp = Dispatcher()

    db = DBService(make_session_factory(s.database_url))
    tx = TransmissionService(s.transmission_conn, s.transmission_user, s.transmission_pass)

    dp.message.middleware(AuthMiddleware(set(s.admin_user_ids)))
    dp.callback_query.middleware(AuthMiddleware(set(s.admin_user_ids)))
    dp.message.middleware(ThrottleMiddleware(s.throttle_seconds))
    dp.callback_query.middleware(ThrottleMiddleware(s.throttle_seconds))

    dp["db"] = db
    dp["tx"] = tx
    dp["config_dirs"] = y.download_dirs

    dp.include_router(router)

    monitor = Monitor(db=db, tx=tx, bot=bot, interval=s.poll_interval_seconds)
    monitor.start()
    try:
        await dp.start_polling(bot)
    finally:
        await monitor.stop()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
