# Copyright (c) 2026 Any1Key
from __future__ import annotations

from typing import Final

Lang = str
SUPPORTED_LANGS: Final[set[str]] = {"ru", "en"}

_TEXTS: Final[dict[str, dict[str, str]]] = {
    "menu.title": {
        "ru": "🏠 *Главное меню*\nВыберите раздел ниже\\.",
        "en": "🏠 *Main menu*\nChoose a section below\\.",
    },
    "cancel.done": {"ru": "❌ Действие отменено\\.", "en": "❌ Action canceled\\."},
    "warn.duplicate": {"ru": "⚠️ Такой торрент уже есть в истории\\.", "en": "⚠️ This torrent is already in history\\."},
    "added.pick_dir": {
        "ru": "✅ *{name}*\nВыберите папку загрузки\\.",
        "en": "✅ *{name}*\nChoose a download folder\\.",
    },
    "err.add_torrent_file": {
        "ru": "⚠️ Не удалось добавить torrent\\-файл в Transmission\\.",
        "en": "⚠️ Failed to add the torrent file to Transmission\\.",
    },
    "err.process_torrent_file": {"ru": "⚠️ Ошибка обработки torrent\\-файла\\.", "en": "⚠️ Error while processing the torrent file\\."},
    "pick.not_found": {"ru": "Папка не найдена\\.", "en": "Folder not found\\."},
    "pick.ok": {"ru": "ОК", "en": "OK"},
    "pick.summary_title": {"ru": "✅ *Торрент запущен*", "en": "✅ *Torrent started*"},
    "pick.folder": {"ru": "Папка", "en": "Folder"},
    "pick.file": {"ru": "Файл", "en": "File"},
    "pick.size": {"ru": "Размер", "en": "Size"},
    "pick.added_at": {"ru": "Добавлен", "en": "Added at"},
    "pick.path": {"ru": "Путь", "en": "Path"},
    "pick.unknown": {"ru": "неизвестно", "en": "unknown"},
    "pick.cancelled": {"ru": "❌ Добавление торрента отменено\\.", "en": "❌ Torrent adding canceled\\."},
    "pick.cancel_failed": {"ru": "⚠️ Не удалось отменить добавление\\.", "en": "⚠️ Failed to cancel adding\\."},
    "pick.already_processed": {"ru": "⚠️ Этот торрент уже обработан\\.", "en": "⚠️ This torrent is already processed\\."},
    "folders.title": {"ru": "🗂️ *Папки загрузки*", "en": "🗂️ *Download folders*"},
    "folders.empty": {"ru": "⚠️ Папки пока не настроены\\.", "en": "⚠️ Folders are not configured yet\\."},
    "history.empty": {"ru": "📜 *История пуста*", "en": "📜 *History is empty*"},
    "history.title": {"ru": "📜 *История* \\[{page}/{pages}\\]", "en": "📜 *History* \\[{page}/{pages}\\]"},
    "stats.fetch_failed": {
        "ru": "⚠️ Не удалось получить статистику Transmission\\.",
        "en": "⚠️ Failed to fetch Transmission stats\\.",
    },
    "stats.fetch_failed_short": {"ru": "⚠️ Не удалось получить статистику\\.", "en": "⚠️ Failed to fetch stats\\."},
    "stats.title": {"ru": "📊 *Статистика Transmission*", "en": "📊 *Transmission Stats*"},
    "stats.downloaded": {"ru": "⬇️ Скачано", "en": "⬇️ Downloaded"},
    "stats.uploaded": {"ru": "⬆️ Отдано", "en": "⬆️ Uploaded"},
    "stats.dl_speed": {"ru": "🚀 Скорость DL", "en": "🚀 DL speed"},
    "stats.ul_speed": {"ru": "🚀 Скорость UL", "en": "🚀 UL speed"},
    "stats.active": {"ru": "🧩 Активно", "en": "🧩 Active"},
    "incomplete.none": {
        "ru": "✅ *Недокачанных нет*\nВсе загрузки завершены\\.",
        "en": "✅ *No incomplete torrents*\nAll downloads are finished\\.",
    },
    "incomplete.title": {"ru": "⬇️ *Недокачанные торренты*", "en": "⬇️ *Incomplete torrents*"},
    "incomplete.fetch_failed": {
        "ru": "⚠️ Не удалось получить список недокачанных\\.",
        "en": "⚠️ Failed to fetch incomplete torrents\\.",
    },
    "incomplete.fetch_failed_short": {"ru": "⚠️ Ошибка загрузки списка\\.", "en": "⚠️ Failed to load the list\\."},
    "incomplete.resume_one_failed": {"ru": "⚠️ Не удалось запустить торрент\\.", "en": "⚠️ Failed to start torrent\\."},
    "incomplete.resume_one_sent": {"ru": "▶️ Команда запуска отправлена\\.", "en": "▶️ Start command sent\\."},
    "incomplete.resume_all_sent": {"ru": "▶️ Запущено: *{count}*", "en": "▶️ Started: *{count}*"},
    "pause.done": {"ru": "⏸️ Поставлено на паузу: *{count}*", "en": "⏸️ Paused: *{count}*"},
    "resume.done": {"ru": "▶️ Возобновлено: *{count}*", "en": "▶️ Resumed: *{count}*"},
    "lang.choose": {"ru": "🌐 *Язык интерфейса*", "en": "🌐 *Interface Language*"},
    "lang.changed": {"ru": "✅ Язык переключен: русский\\.", "en": "✅ Language switched: English\\."},
    "maintenance.title": {
        "ru": "🛠️ *Обслуживание*\nВыберите действие\\.",
        "en": "🛠️ *Maintenance*\nChoose an action\\.",
    },
    "maintenance.cleanup_missing_done": {
        "ru": "🧹 Удалено записей `missing`: *{count}*",
        "en": "🧹 Deleted `missing` records: *{count}*",
    },
    "maintenance.cleanup_stale_done": {
        "ru": "🧹 Удалено устаревших pending \\(>{hours} ч\\): *{count}*",
        "en": "🧹 Deleted stale pending \\(>{hours}h\\): *{count}*",
    },
    "maintenance.cleanup_failed": {
        "ru": "⚠️ Ошибка обслуживания\\.",
        "en": "⚠️ Maintenance failed\\.",
    },
    "btn.stats": {"ru": "📊 Статистика", "en": "📊 Stats"},
    "btn.folders": {"ru": "🗂️ Папки", "en": "🗂️ Folders"},
    "btn.history": {"ru": "📜 История", "en": "📜 History"},
    "btn.incomplete": {"ru": "⬇️ Недокачанные", "en": "⬇️ Incomplete"},
    "btn.pause_all": {"ru": "⏸️ Пауза всего", "en": "⏸️ Pause all"},
    "btn.resume_all": {"ru": "▶️ Продолжить все", "en": "▶️ Resume all"},
    "btn.open_menu": {"ru": "🏠 Меню", "en": "🏠 Menu"},
    "btn.language": {"ru": "🌐 Язык", "en": "🌐 Language"},
    "btn.refresh_stats": {"ru": "🔄 Обновить", "en": "🔄 Refresh"},
    "btn.main_menu": {"ru": "🏠 Главное меню", "en": "🏠 Main menu"},
    "btn.cancel_to_menu": {
        "ru": "❌ Отменить",
        "en": "❌ Cancel",
    },
    "btn.back": {"ru": "⬅️ Назад", "en": "⬅️ Back"},
    "btn.forward": {"ru": "Вперёд ➡️", "en": "Next ➡️"},
    "btn.pick": {"ru": "{name}", "en": "{name}"},
    "btn.resume": {"ru": "▶️ {name} • {progress}%", "en": "▶️ {name} • {progress}%"},
    "btn.resume_incomplete_all": {
        "ru": "▶️ Продолжить все",
        "en": "▶️ Resume all",
    },
    "btn.refresh_list": {"ru": "🔄 Обновить", "en": "🔄 Refresh"},
    "btn.maintenance_cleanup_missing": {"ru": "🧹 Очистить missing", "en": "🧹 Cleanup missing"},
    "btn.maintenance_cleanup_stale": {"ru": "🧹 Очистить stale", "en": "🧹 Cleanup stale"},
    "auth.denied": {"ru": "⛔ Доступ запрещен\\.", "en": "⛔ Access denied\\."},
    "throttle.wait": {"ru": "⏳ Подождите немного\\.", "en": "⏳ Please wait a moment\\."},
}


def normalize_lang(raw: str | None) -> Lang:
    if not raw:
        return "ru"
    x = raw.lower()
    if x.startswith("en"):
        return "en"
    if x.startswith("ru"):
        return "ru"
    return "ru"


def t(key: str, lang: Lang, **kwargs: object) -> str:
    pack = _TEXTS.get(key, {})
    base = pack.get(lang) or pack.get("ru") or key
    if kwargs:
        return base.format(**kwargs)
    return base


def all_button_variants(key: str) -> list[str]:
    pack = _TEXTS.get(key, {})
    return [pack[k] for k in ("ru", "en") if k in pack]
