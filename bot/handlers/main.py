# Copyright (c) 2026 Any1Key
from __future__ import annotations

import tempfile
from pathlib import Path

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.keyboards import dir_kb, folders_kb, history_kb, incomplete_kb, menu_kb, stats_kb
from bot.services.db import DBService
from bot.services.transmission import TransmissionService
from bot.utils import esc, human

router = Router()
PAGE_SIZE = 8


def _dirs(cfg: dict[str, str]) -> list[tuple[str, str]]:
    return list(cfg.items())


def _incomplete_text(items: list[dict[str, object]]) -> str:
    if not items:
        return "✅ *Недокачанных торрентов нет*\n🎉 Все загрузки завершены"
    lines = ["⬇️ *Недокачанные торренты*", "━━━━━━━━━━━━━━"]
    for i, item in enumerate(items[:15], start=1):
        name = esc(str(item["name"]))
        progress = int(item["progress"])
        status = esc(str(item["status"]))
        lines.append(f"{i}\\. 🧩 *{name}* \\({progress}%\\) \\| `{status}`")
    return "\n".join(lines)


@router.message(Command("start"))
@router.message(Command("menu"))
@router.message(F.text == "🏠 Главное меню")
@router.message(F.text == "🏠 Открыть главное меню")
async def start(message: Message) -> None:
    await message.answer(
        "🏠 *Главное меню*\n"
        "━━━━━━━━━━━━━━\n"
        "Выберите нужный раздел ниже 👇",
        reply_markup=menu_kb(),
    )


@router.callback_query(F.data == "menu")
async def menu_cb(callback: CallbackQuery) -> None:
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(
        "🏠 *Главное меню*\n"
        "━━━━━━━━━━━━━━\n"
        "Выберите нужный раздел ниже 👇",
        reply_markup=menu_kb(),
    )
    await callback.answer()


@router.message(Command("cancel"))
async def cancel(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("❌ Отменено", reply_markup=menu_kb())


@router.message(F.text.startswith("magnet:?"))
async def magnet(message: Message, tx: TransmissionService, db: DBService, config_dirs: dict[str, str]) -> None:
    h, n = await tx.add_magnet((message.text or "").strip())
    try:
        await db.add_torrent(message.from_user.id, h, n)
    except ValueError as exc:
        if str(exc) == "torrent_already_exists":
            await message.answer("⚠️ Такой торрент уже добавлен ранее")
            return
        raise
    await message.answer(f"✅ Добавлено *{esc(n)}*\nВыберите папку:", reply_markup=dir_kb(h, _dirs(config_dirs)))


@router.message(F.document)
async def torrent_file(message: Message, tx: TransmissionService, db: DBService, config_dirs: dict[str, str]) -> None:
    doc = message.document
    if not doc or not (doc.file_name or "").lower().endswith(".torrent"):
        return
    try:
        f = await message.bot.get_file(doc.file_id)
        with tempfile.NamedTemporaryFile(suffix=".torrent", delete=False) as tmp:
            fp = Path(tmp.name)
        await message.bot.download_file(f.file_path, destination=fp)
        try:
            h, n = await tx.add_file(fp)
        except Exception as exc:
            await message.answer(f"⚠️ {esc('Не удалось добавить torrent файл в Transmission')}\n`{esc(str(exc))}`")
            return
    except Exception as exc:
        await message.answer(f"⚠️ {esc('Ошибка при обработке torrent файла')}\n`{esc(str(exc))}`")
        return
    finally:
        if "fp" in locals():
            fp.unlink(missing_ok=True)
    try:
        await db.add_torrent(message.from_user.id, h, n)
    except ValueError as exc:
        if str(exc) == "torrent_already_exists":
            await message.answer("⚠️ Такой торрент уже добавлен ранее")
            return
        raise
    await message.answer(f"✅ Добавлено *{esc(n)}*\nВыберите папку:", reply_markup=dir_kb(h, _dirs(config_dirs)))


@router.callback_query(F.data.startswith("pick:"))
async def pick(callback: CallbackQuery, tx: TransmissionService, db: DBService, config_dirs: dict[str, str]) -> None:
    _, h, i_s = callback.data.split(":")
    i = int(i_s)
    dirs = _dirs(config_dirs)
    if not (0 <= i < len(dirs)):
        await callback.answer("Папка не найдена", show_alert=True)
        return
    name, path = dirs[i]
    await tx.set_dir_and_start(h, path)
    await db.set_torrent_dir(h, path)
    # Одноразовые кнопки: после выбора папки убираем клавиатуру.
    await callback.message.edit_text(f"▶️ *{esc(name)}*\n`{esc(path)}`")
    await callback.answer("ОК")


@router.message(Command("folders"))
@router.message(F.text == "📁 Папки")
@router.message(F.text == "🗂️ Системные папки")
@router.callback_query(F.data == "folders")
async def folders(event: Message | CallbackQuery, config_dirs: dict[str, str]) -> None:
    lines = ["🗂️ *Системные папки загрузки*", "━━━━━━━━━━━━━━"]

    if config_dirs:
        lines.append("")
        for name, path in config_dirs.items():
            lines.append(f"📁 *{esc(name)}*")
            lines.append(f"↳ `{esc(path)}`")
    else:
        lines.append("")
        lines.append("⚠️ Системные папки пока не настроены")

    text = "\n".join(lines)

    if isinstance(event, Message):
        await event.answer(text, reply_markup=folders_kb())
    else:
        await event.message.edit_text(text, reply_markup=folders_kb())
        await event.answer()


@router.message(Command("history"))
@router.message(F.text == "📜 История")
@router.message(F.text == "📜 История загрузок")
@router.callback_query(F.data.startswith("history:"))
async def history(event: Message | CallbackQuery, db: DBService) -> None:
    uid = event.from_user.id  # type: ignore[union-attr]
    page = 1
    if isinstance(event, CallbackQuery):
        page = int(event.data.split(":")[1])
    items, total = await db.history(uid, page, PAGE_SIZE)
    pages = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)
    if not items:
        txt = "📜 *История загрузок пуста*"
    else:
        lines=[f"📜 *История загрузок* \\({page}/{pages}\\)", "━━━━━━━━━━━━━━"]
        for t in items:
            lines.append(f"🎬 *{esc(t.torrent_name)}* \\| `{esc(t.status)}`")
        txt="\n".join(lines)
    if isinstance(event, Message):
        await event.answer(txt, reply_markup=history_kb(page, pages))
    else:
        await event.message.edit_text(txt, reply_markup=history_kb(page, pages))
        await event.answer()


@router.message(Command("stats"))
@router.message(F.text == "📊 Статистика")
@router.message(F.text == "📊 Статистика сети")
@router.callback_query(F.data == "stats")
async def stats(event: Message | CallbackQuery, tx: TransmissionService) -> None:
    try:
        s = await tx.stats()
    except Exception:
        if isinstance(event, Message):
            await event.answer("⚠️ Не удалось получить статистику Transmission")
        else:
            await event.answer("⚠️ Не удалось получить статистику", show_alert=True)
        return

    txt = (
        "📊 *Статистика сети*\n"
        "━━━━━━━━━━━━━━\n"
        f"⬇️ Скачано: {esc(human(s['downloaded']))}\n"
        f"⬆️ Отдано: {esc(human(s['uploaded']))}\n"
        f"🚀 Скорость DL: {esc(human(s['download_speed']))}/s\n"
        f"🚀 Скорость UL: {esc(human(s['upload_speed']))}/s\n"
        f"🧩 Активных торрентов: {s['active']}"
    )
    if isinstance(event, Message):
        await event.answer(txt, reply_markup=stats_kb())
    else:
        try:
            await event.message.edit_text(txt, reply_markup=stats_kb())
        except TelegramBadRequest as exc:
            if "message is not modified" not in str(exc).lower():
                raise
        await event.answer()


@router.message(Command("incomplete"))
@router.message(F.text == "⬇️ Недокачанные")
@router.message(F.text == "⬇️ Недокачанные торренты")
@router.callback_query(F.data == "incomplete:refresh")
async def incomplete(event: Message | CallbackQuery, tx: TransmissionService) -> None:
    try:
        items = await tx.incomplete()
    except Exception:
        if isinstance(event, Message):
            await event.answer("⚠️ Не удалось получить список недокачанных")
        else:
            await event.answer("⚠️ Ошибка загрузки списка", show_alert=True)
        return

    text = _incomplete_text(items)
    kb = incomplete_kb(items)
    if isinstance(event, Message):
        await event.answer(text, reply_markup=kb)
    else:
        await event.message.edit_text(text, reply_markup=kb)
        await event.answer()


@router.callback_query(F.data.startswith("incomplete:resume:"))
async def incomplete_resume_one(callback: CallbackQuery, tx: TransmissionService) -> None:
    torrent_hash = callback.data.split(":", maxsplit=2)[2]
    try:
        await tx.resume_one(torrent_hash)
    except Exception:
        await callback.answer("⚠️ Не удалось запустить торрент", show_alert=True)
        return
    await callback.answer("▶️ Запуск отправлен")
    items = await tx.incomplete()
    await callback.message.edit_text(_incomplete_text(items), reply_markup=incomplete_kb(items))


@router.callback_query(F.data == "incomplete:resume_all")
async def incomplete_resume_all(callback: CallbackQuery, tx: TransmissionService) -> None:
    count = await tx.resume_all()
    await callback.answer(f"▶️ Запущено: {count}")
    items = await tx.incomplete()
    await callback.message.edit_text(_incomplete_text(items), reply_markup=incomplete_kb(items))


@router.callback_query(F.data == "admin:pause")
@router.message(F.text == "⏸️ Приостановить все")
@router.message(F.text == "⏸️ Пауза всех торрентов")
async def pause(event: Message | CallbackQuery, tx: TransmissionService) -> None:
    c = await tx.pause_all()
    if isinstance(event, Message):
        await event.answer(f"⏸️ Остановлено: *{c}*", reply_markup=menu_kb())
    else:
        await event.message.edit_reply_markup(reply_markup=None)
        await event.answer()
        await event.message.answer(f"⏸️ Остановлено: *{c}*", reply_markup=menu_kb())


@router.callback_query(F.data == "admin:resume")
@router.message(F.text == "▶️ Возобновить все")
@router.message(F.text == "▶️ Продолжить все торренты")
async def resume(event: Message | CallbackQuery, tx: TransmissionService) -> None:
    c = await tx.resume_all()
    if isinstance(event, Message):
        await event.answer(f"▶️ Запущено: *{c}*", reply_markup=menu_kb())
    else:
        await event.message.edit_reply_markup(reply_markup=None)
        await event.answer()
        await event.message.answer(f"▶️ Запущено: *{c}*", reply_markup=menu_kb())
