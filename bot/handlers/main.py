# Copyright (c) 2026 Any1Key
from __future__ import annotations

import tempfile
from pathlib import Path

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.i18n import all_button_variants, t
from bot.keyboards import dir_kb, folders_kb, history_kb, incomplete_kb, language_kb, menu_kb, stats_kb
from bot.services.db import DBService
from bot.services.transmission import TransmissionService
from bot.utils import esc, human

router = Router()
PAGE_SIZE = 8


def _dirs(cfg: dict[str, str]) -> list[tuple[str, str]]:
    return list(cfg.items())


async def _lang(event: Message | CallbackQuery, db: DBService) -> str:
    return await db.ensure_user_lang(event.from_user.id, getattr(event.from_user, "language_code", None))


def _incomplete_text(items: list[dict[str, object]], lang: str) -> str:
    if not items:
        return t("incomplete.none", lang)
    lines = [t("incomplete.title", lang), "━━━━━━━━━━━━━━"]
    for i, item in enumerate(items[:15], start=1):
        name = esc(str(item["name"]))
        progress = int(item["progress"])
        status = esc(str(item["status"]))
        lines.append(f"{i}\\. 🧩 *{name}* \\({progress}%\\) \\| `{status}`")
    return "\n".join(lines)


@router.message(Command("start"))
@router.message(Command("menu"))
@router.message(F.text == "🏠 Главное меню")
@router.message(F.text.in_(all_button_variants("btn.open_menu")))
async def start(message: Message, db: DBService) -> None:
    lang = await _lang(message, db)
    await message.answer(
        t("menu.title", lang),
        reply_markup=menu_kb(lang),
    )


@router.callback_query(F.data == "menu")
async def menu_cb(callback: CallbackQuery, db: DBService) -> None:
    lang = await _lang(callback, db)
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(
        t("menu.title", lang),
        reply_markup=menu_kb(lang),
    )
    await callback.answer()


@router.message(Command("cancel"))
async def cancel(message: Message, state: FSMContext, db: DBService) -> None:
    lang = await _lang(message, db)
    await state.clear()
    await message.answer(t("cancel.done", lang), reply_markup=menu_kb(lang))


@router.message(Command("language"))
@router.message(F.text.in_(all_button_variants("btn.language")))
async def language_menu(message: Message, db: DBService) -> None:
    lang = await _lang(message, db)
    await message.answer(t("lang.choose", lang), reply_markup=language_kb(lang))


@router.callback_query(F.data.startswith("lang:set:"))
async def language_set(callback: CallbackQuery, db: DBService) -> None:
    lang = callback.data.split(":")[-1]
    lang = await db.set_user_lang(callback.from_user.id, lang)
    await callback.answer()
    await callback.message.edit_text(t("lang.changed", lang), reply_markup=None)
    await callback.message.answer(t("menu.title", lang), reply_markup=menu_kb(lang))


@router.message(F.text.startswith("magnet:?"))
async def magnet(message: Message, tx: TransmissionService, db: DBService, config_dirs: dict[str, str]) -> None:
    lang = await _lang(message, db)
    h, n = await tx.add_magnet((message.text or "").strip())
    try:
        await db.add_torrent(message.from_user.id, h, n)
    except ValueError as exc:
        if str(exc) == "torrent_already_exists":
            await message.answer(t("warn.duplicate", lang))
            return
        raise
    await message.answer(t("added.pick_dir", lang, name=esc(n)), reply_markup=dir_kb(h, _dirs(config_dirs), lang))


@router.message(F.document)
async def torrent_file(message: Message, tx: TransmissionService, db: DBService, config_dirs: dict[str, str]) -> None:
    lang = await _lang(message, db)
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
            await message.answer(f"{t('err.add_torrent_file', lang)}\n`{esc(str(exc))}`")
            return
    except Exception as exc:
        await message.answer(f"{t('err.process_torrent_file', lang)}\n`{esc(str(exc))}`")
        return
    finally:
        if "fp" in locals():
            fp.unlink(missing_ok=True)
    try:
        await db.add_torrent(message.from_user.id, h, n)
    except ValueError as exc:
        if str(exc) == "torrent_already_exists":
            await message.answer(t("warn.duplicate", lang))
            return
        raise
    await message.answer(t("added.pick_dir", lang, name=esc(n)), reply_markup=dir_kb(h, _dirs(config_dirs), lang))


@router.callback_query(F.data.startswith("pick:"))
async def pick(callback: CallbackQuery, tx: TransmissionService, db: DBService, config_dirs: dict[str, str]) -> None:
    lang = await _lang(callback, db)
    _, h, i_s = callback.data.split(":")
    i = int(i_s)
    dirs = _dirs(config_dirs)
    if not (0 <= i < len(dirs)):
        await callback.answer(t("pick.not_found", lang), show_alert=True)
        return
    name, path = dirs[i]
    await tx.set_dir_and_start(h, path)
    await db.set_torrent_dir(h, path)
    # Одноразовые кнопки: после выбора папки убираем клавиатуру.
    await callback.message.edit_text(f"▶️ *{esc(name)}*\n`{esc(path)}`")
    await callback.answer(t("pick.ok", lang))


@router.message(Command("folders"))
@router.message(F.text == "📁 Папки")
@router.message(F.text.in_(all_button_variants("btn.folders")))
@router.callback_query(F.data == "folders")
async def folders(event: Message | CallbackQuery, db: DBService, config_dirs: dict[str, str]) -> None:
    lang = await _lang(event, db)
    lines = [t("folders.title", lang), "━━━━━━━━━━━━━━"]

    if config_dirs:
        lines.append("")
        for name, path in config_dirs.items():
            lines.append(f"📁 *{esc(name)}*")
            lines.append(f"↳ `{esc(path)}`")
    else:
        lines.append("")
        lines.append(t("folders.empty", lang))

    text = "\n".join(lines)

    if isinstance(event, Message):
        await event.answer(text, reply_markup=folders_kb(lang))
    else:
        await event.message.edit_text(text, reply_markup=folders_kb(lang))
        await event.answer()


@router.message(Command("history"))
@router.message(F.text == "📜 История")
@router.message(F.text.in_(all_button_variants("btn.history")))
@router.callback_query(F.data.startswith("history:"))
async def history(event: Message | CallbackQuery, db: DBService) -> None:
    lang = await _lang(event, db)
    uid = event.from_user.id  # type: ignore[union-attr]
    page = 1
    if isinstance(event, CallbackQuery):
        page = int(event.data.split(":")[1])
    items, total = await db.history(uid, page, PAGE_SIZE)
    pages = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)
    if not items:
        txt = t("history.empty", lang)
    else:
        lines=[t("history.title", lang, page=page, pages=pages), "━━━━━━━━━━━━━━"]
        for item in items:
            lines.append(f"🎬 *{esc(item.torrent_name)}* \\| `{esc(item.status)}`")
        txt="\n".join(lines)
    if isinstance(event, Message):
        await event.answer(txt, reply_markup=history_kb(page, pages, lang))
    else:
        try:
            await event.message.edit_text(txt, reply_markup=history_kb(page, pages, lang))
        except TelegramBadRequest as exc:
            if "message is not modified" not in str(exc).lower():
                raise
        await event.answer()


@router.message(Command("stats"))
@router.message(F.text == "📊 Статистика")
@router.message(F.text.in_(all_button_variants("btn.stats")))
@router.callback_query(F.data == "stats")
async def stats(event: Message | CallbackQuery, tx: TransmissionService, db: DBService) -> None:
    lang = await _lang(event, db)
    try:
        s = await tx.stats()
    except Exception:
        if isinstance(event, Message):
            await event.answer(t("stats.fetch_failed", lang))
        else:
            await event.answer(t("stats.fetch_failed_short", lang), show_alert=True)
        return

    txt = (
        f"{t('stats.title', lang)}\n"
        "━━━━━━━━━━━━━━\n"
        f"{t('stats.downloaded', lang)}: {esc(human(s['downloaded']))}\n"
        f"{t('stats.uploaded', lang)}: {esc(human(s['uploaded']))}\n"
        f"{t('stats.dl_speed', lang)}: {esc(human(s['download_speed']))}/s\n"
        f"{t('stats.ul_speed', lang)}: {esc(human(s['upload_speed']))}/s\n"
        f"{t('stats.active', lang)}: {s['active']}"
    )
    if isinstance(event, Message):
        await event.answer(txt, reply_markup=stats_kb(lang))
    else:
        try:
            await event.message.edit_text(txt, reply_markup=stats_kb(lang))
        except TelegramBadRequest as exc:
            if "message is not modified" not in str(exc).lower():
                raise
        await event.answer()


@router.message(Command("incomplete"))
@router.message(F.text == "⬇️ Недокачанные")
@router.message(F.text.in_(all_button_variants("btn.incomplete")))
@router.callback_query(F.data == "incomplete:refresh")
async def incomplete(event: Message | CallbackQuery, tx: TransmissionService, db: DBService) -> None:
    lang = await _lang(event, db)
    try:
        items = await tx.incomplete()
    except Exception:
        if isinstance(event, Message):
            await event.answer(t("incomplete.fetch_failed", lang))
        else:
            await event.answer(t("incomplete.fetch_failed_short", lang), show_alert=True)
        return

    text = _incomplete_text(items, lang)
    kb = incomplete_kb(items, lang)
    if isinstance(event, Message):
        await event.answer(text, reply_markup=kb)
    else:
        await event.message.edit_text(text, reply_markup=kb)
        await event.answer()


@router.callback_query(F.data.startswith("incomplete:resume:"))
async def incomplete_resume_one(callback: CallbackQuery, tx: TransmissionService, db: DBService) -> None:
    lang = await _lang(callback, db)
    torrent_hash = callback.data.split(":", maxsplit=2)[2]
    try:
        await tx.resume_one(torrent_hash)
    except Exception:
        await callback.answer(t("incomplete.resume_one_failed", lang), show_alert=True)
        return
    await callback.answer(t("incomplete.resume_one_sent", lang))
    items = await tx.incomplete()
    await callback.message.edit_text(_incomplete_text(items, lang), reply_markup=incomplete_kb(items, lang))


@router.callback_query(F.data == "incomplete:resume_all")
async def incomplete_resume_all(callback: CallbackQuery, tx: TransmissionService, db: DBService) -> None:
    lang = await _lang(callback, db)
    count = await tx.resume_all()
    await callback.answer(t("incomplete.resume_all_sent", lang, count=count))
    items = await tx.incomplete()
    await callback.message.edit_text(_incomplete_text(items, lang), reply_markup=incomplete_kb(items, lang))


@router.callback_query(F.data == "admin:pause")
@router.message(F.text == "⏸️ Приостановить все")
@router.message(F.text.in_(all_button_variants("btn.pause_all")))
async def pause(event: Message | CallbackQuery, tx: TransmissionService, db: DBService) -> None:
    lang = await _lang(event, db)
    c = await tx.pause_all()
    if isinstance(event, Message):
        await event.answer(t("pause.done", lang, count=c), reply_markup=menu_kb(lang))
    else:
        await event.message.edit_reply_markup(reply_markup=None)
        await event.answer()
        await event.message.answer(t("pause.done", lang, count=c), reply_markup=menu_kb(lang))


@router.callback_query(F.data == "admin:resume")
@router.message(F.text == "▶️ Возобновить все")
@router.message(F.text.in_(all_button_variants("btn.resume_all")))
async def resume(event: Message | CallbackQuery, tx: TransmissionService, db: DBService) -> None:
    lang = await _lang(event, db)
    c = await tx.resume_all()
    if isinstance(event, Message):
        await event.answer(t("resume.done", lang, count=c), reply_markup=menu_kb(lang))
    else:
        await event.message.edit_reply_markup(reply_markup=None)
        await event.answer()
        await event.message.answer(t("resume.done", lang, count=c), reply_markup=menu_kb(lang))
