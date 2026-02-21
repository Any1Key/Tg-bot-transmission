from __future__ import annotations

import tempfile
from pathlib import Path

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.handlers.states import AddDirState
from bot.keyboards import dir_kb, history_kb, menu_kb, stats_kb
from bot.services.db import DBService
from bot.services.docker_control import DockerControlService
from bot.services.transmission import TransmissionService
from bot.utils import esc, human

router = Router()
PAGE_SIZE = 8


def _dirs(cfg: dict[str, str], user_dirs: list[tuple[str, str]]) -> list[tuple[str, str]]:
    return list(cfg.items()) + user_dirs


@router.message(Command("start"))
@router.message(Command("menu"))
async def start(message: Message) -> None:
    await message.answer("🏠 *Главное меню*", reply_markup=menu_kb())


@router.callback_query(F.data == "menu")
async def menu_cb(callback: CallbackQuery) -> None:
    await callback.message.edit_text("🏠 *Главное меню*", reply_markup=menu_kb())
    await callback.answer()


@router.message(Command("cancel"))
async def cancel(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("❌ Отменено")


@router.message(F.text.startswith("magnet:?"))
async def magnet(message: Message, tx: TransmissionService, db: DBService, config_dirs: dict[str, str]) -> None:
    h, n = await tx.add_magnet((message.text or "").strip())
    await db.add_torrent(message.from_user.id, h, n)
    user_dirs = [(d.name, d.path) for d in await db.user_dirs(message.from_user.id)]
    await message.answer(f"✅ Добавлено *{esc(n)}*\nВыберите папку:", reply_markup=dir_kb(h, _dirs(config_dirs, user_dirs)))


@router.message(F.document)
async def torrent_file(message: Message, tx: TransmissionService, db: DBService, config_dirs: dict[str, str]) -> None:
    doc = message.document
    if not doc or not (doc.file_name or "").lower().endswith(".torrent"):
        return
    f = await message.bot.get_file(doc.file_id)
    with tempfile.NamedTemporaryFile(suffix=".torrent", delete=False) as tmp:
        fp = Path(tmp.name)
    await message.bot.download_file(f.file_path, destination=fp)
    try:
        h, n = await tx.add_file(fp)
    finally:
        fp.unlink(missing_ok=True)
    await db.add_torrent(message.from_user.id, h, n)
    user_dirs = [(d.name, d.path) for d in await db.user_dirs(message.from_user.id)]
    await message.answer(f"✅ Добавлено *{esc(n)}*\nВыберите папку:", reply_markup=dir_kb(h, _dirs(config_dirs, user_dirs)))


@router.callback_query(F.data.startswith("pick:"))
async def pick(callback: CallbackQuery, tx: TransmissionService, db: DBService, config_dirs: dict[str, str]) -> None:
    _, h, i_s = callback.data.split(":")
    i = int(i_s)
    user_dirs = [(d.name, d.path) for d in await db.user_dirs(callback.from_user.id)]
    dirs = _dirs(config_dirs, user_dirs)
    if not (0 <= i < len(dirs)):
        await callback.answer("Папка не найдена", show_alert=True)
        return
    name, path = dirs[i]
    await tx.set_dir_and_start(h, path)
    await db.set_torrent_dir(h, path)
    await callback.message.edit_text(f"▶️ *{esc(name)}*\n`{esc(path)}`")
    await callback.answer("ОК")


@router.message(Command("history"))
@router.callback_query(F.data.startswith("history:"))
async def history(event: Message | CallbackQuery, db: DBService) -> None:
    uid = event.from_user.id  # type: ignore[union-attr]
    page = 1
    if isinstance(event, CallbackQuery):
        page = int(event.data.split(":")[1])
    items, total = await db.history(uid, page, PAGE_SIZE)
    pages = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)
    if not items:
        txt = "📜 *История пуста*"
    else:
        lines=[f"📜 *История* \\({page}/{pages}\\)"]
        for t in items:
            lines.append(f"• *{esc(t.torrent_name)}* | `{esc(t.status)}`")
        txt="\n".join(lines)
    if isinstance(event, Message):
        await event.answer(txt, reply_markup=history_kb(page, pages))
    else:
        await event.message.edit_text(txt, reply_markup=history_kb(page, pages))
        await event.answer()


@router.message(Command("stats"))
@router.callback_query(F.data == "stats")
async def stats(event: Message | CallbackQuery, tx: TransmissionService) -> None:
    s = await tx.stats()
    txt = (
        "📊 *Статистика*\n"
        f"⬇️ {esc(human(s['downloaded']))}\n"
        f"⬆️ {esc(human(s['uploaded']))}\n"
        f"🚀 DL {esc(human(s['download_speed']))}/s\n"
        f"🚀 UL {esc(human(s['upload_speed']))}/s\n"
        f"🧩 {s['active']}"
    )
    if isinstance(event, Message):
        await event.answer(txt, reply_markup=stats_kb())
    else:
        await event.message.edit_text(txt, reply_markup=stats_kb())
        await event.answer()


@router.callback_query(F.data == "admin:pause")
async def pause(callback: CallbackQuery, tx: TransmissionService) -> None:
    c = await tx.pause_all()
    await callback.answer()
    await callback.message.answer(f"⏸️ Остановлено: *{c}*")


@router.callback_query(F.data == "admin:resume")
async def resume(callback: CallbackQuery, tx: TransmissionService) -> None:
    c = await tx.resume_all()
    await callback.answer()
    await callback.message.answer(f"▶️ Запущено: *{c}*")


@router.callback_query(F.data == "admin:restart")
async def restart(callback: CallbackQuery, docker_control: DockerControlService, transmission_container_name: str) -> None:
    await docker_control.restart(transmission_container_name)
    await callback.answer("Перезапущено")
