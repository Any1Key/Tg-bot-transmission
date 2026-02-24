# Copyright (c) 2026 Any1Key
from __future__ import annotations

from typing import Final

Lang = str
SUPPORTED_LANGS: Final[set[str]] = {"ru", "en"}

_TEXTS: Final[dict[str, dict[str, str]]] = {
    "menu.title": {
        "ru": "🏠 *Главное меню*\n━━━━━━━━━━━━━━\nВыберите нужный раздел ниже 👇",
        "en": "🏠 *Main Menu*\n━━━━━━━━━━━━━━\nChoose an option below 👇",
    },
    "cancel.done": {"ru": "❌ Отменено", "en": "❌ Canceled"},
    "warn.duplicate": {"ru": "⚠️ Такой торрент уже добавлен ранее", "en": "⚠️ This torrent was already added"},
    "added.pick_dir": {
        "ru": "✅ Для начала скачивания *{name}*, выберите папку для загрузки:",
        "en": "✅ To start downloading *{name}*, choose a destination folder:",
    },
    "err.add_torrent_file": {
        "ru": "⚠️ Не удалось добавить torrent файл в Transmission",
        "en": "⚠️ Failed to add .torrent file to Transmission",
    },
    "err.process_torrent_file": {"ru": "⚠️ Ошибка при обработке torrent файла", "en": "⚠️ Error while processing .torrent file"},
    "pick.not_found": {"ru": "Папка не найдена", "en": "Folder not found"},
    "pick.ok": {"ru": "ОК", "en": "OK"},
    "pick.summary_title": {"ru": "✅ *Торрент запущен*", "en": "✅ *Torrent started*"},
    "pick.folder": {"ru": "Папка", "en": "Folder"},
    "pick.file": {"ru": "Файл", "en": "File"},
    "pick.size": {"ru": "Объем", "en": "Size"},
    "pick.added_at": {"ru": "Добавлен", "en": "Added at"},
    "pick.path": {"ru": "Путь", "en": "Path"},
    "pick.unknown": {"ru": "неизвестно", "en": "unknown"},
    "pick.cancelled": {"ru": "❌ Добавление торрента отменено", "en": "❌ Torrent adding canceled"},
    "pick.cancel_failed": {"ru": "⚠️ Не удалось отменить добавление", "en": "⚠️ Failed to cancel adding"},
    "pick.already_processed": {"ru": "⚠️ Этот торрент уже обработан", "en": "⚠️ This torrent was already processed"},
    "folders.title": {"ru": "🗂️ *Системные папки загрузки*", "en": "🗂️ *System Download Folders*"},
    "folders.empty": {"ru": "⚠️ Системные папки пока не настроены", "en": "⚠️ System folders are not configured yet"},
    "history.empty": {"ru": "📜 *История загрузок пуста*", "en": "📜 *Download history is empty*"},
    "history.title": {"ru": "📜 *История загрузок* \\({page}/{pages}\\)", "en": "📜 *Download History* \\({page}/{pages}\\)"},
    "stats.fetch_failed": {
        "ru": "⚠️ Не удалось получить статистику Transmission",
        "en": "⚠️ Failed to fetch Transmission stats",
    },
    "stats.fetch_failed_short": {"ru": "⚠️ Не удалось получить статистику", "en": "⚠️ Failed to fetch stats"},
    "stats.title": {"ru": "📊 *Статистика Transmission*", "en": "📊 *Transmission Stats*"},
    "stats.downloaded": {"ru": "⬇️ Скачано", "en": "⬇️ Downloaded"},
    "stats.uploaded": {"ru": "⬆️ Отдано", "en": "⬆️ Uploaded"},
    "stats.dl_speed": {"ru": "🚀 Скорость DL", "en": "🚀 DL Speed"},
    "stats.ul_speed": {"ru": "🚀 Скорость UL", "en": "🚀 UL Speed"},
    "stats.active": {"ru": "🧩 Активных торрентов", "en": "🧩 Active Torrents"},
    "incomplete.none": {
        "ru": "✅ *Недокачанных торрентов нет*\n🎉 Все загрузки завершены",
        "en": "✅ *No incomplete torrents*\n🎉 All downloads are finished",
    },
    "incomplete.title": {"ru": "⬇️ *Недокачанные торренты*", "en": "⬇️ *Incomplete Torrents*"},
    "incomplete.fetch_failed": {
        "ru": "⚠️ Не удалось получить список недокачанных",
        "en": "⚠️ Failed to fetch incomplete torrents",
    },
    "incomplete.fetch_failed_short": {"ru": "⚠️ Ошибка загрузки списка", "en": "⚠️ Failed to load the list"},
    "incomplete.resume_one_failed": {"ru": "⚠️ Не удалось запустить торрент", "en": "⚠️ Failed to start torrent"},
    "incomplete.resume_one_sent": {"ru": "▶️ Запуск отправлен", "en": "▶️ Start command sent"},
    "incomplete.resume_all_sent": {"ru": "▶️ Запущено: {count}", "en": "▶️ Started: {count}"},
    "pause.done": {"ru": "⏸️ Остановлено: *{count}*", "en": "⏸️ Stopped: *{count}*"},
    "resume.done": {"ru": "▶️ Запущено: *{count}*", "en": "▶️ Started: *{count}*"},
    "lang.choose": {"ru": "🌐 *Язык интерфейса*", "en": "🌐 *Interface Language*"},
    "lang.changed": {"ru": "✅ Язык переключен на русский", "en": "✅ Language switched to English"},
    "maintenance.title": {
        "ru": "🛠️ *Обслуживание*\nВыберите действие:",
        "en": "🛠️ *Maintenance*\nChoose an action:",
    },
    "maintenance.cleanup_missing_done": {
        "ru": "🧹 Удалено записей со статусом `missing`: *{count}*",
        "en": "🧹 Deleted `missing` records: *{count}*",
    },
    "maintenance.cleanup_stale_done": {
        "ru": "🧹 Удалено устаревших pending \\(>{hours}ч\\): *{count}*",
        "en": "🧹 Deleted stale pending \\(>{hours}h\\): *{count}*",
    },
    "maintenance.cleanup_failed": {
        "ru": "⚠️ Ошибка обслуживания",
        "en": "⚠️ Maintenance failed",
    },
    "btn.stats": {"ru": "📊 Статистика Transmission", "en": "📊 Transmission Stats"},
    "btn.folders": {"ru": "🗂️ Системные папки", "en": "🗂️ System Folders"},
    "btn.history": {"ru": "📜 История загрузок", "en": "📜 Download History"},
    "btn.incomplete": {"ru": "⬇️ Недокачанные торренты", "en": "⬇️ Incomplete Torrents"},
    "btn.pause_all": {"ru": "⏸️ Пауза всех торрентов", "en": "⏸️ Pause All Torrents"},
    "btn.resume_all": {"ru": "▶️ Продолжить все торренты", "en": "▶️ Resume All Torrents"},
    "btn.open_menu": {"ru": "🏠 Открыть главное меню", "en": "🏠 Open Main Menu"},
    "btn.language": {"ru": "🌐 Язык", "en": "🌐 Language"},
    "btn.refresh_stats": {"ru": "🔄 Обновить статистику", "en": "🔄 Refresh Stats"},
    "btn.main_menu": {"ru": "🏠 В главное меню", "en": "🏠 Main Menu"},
    "btn.cancel_to_menu": {
        "ru": "❌ Отменить и выйти в Главное меню",
        "en": "❌ Cancel and open Main Menu",
    },
    "btn.back": {"ru": "⬅️ Назад", "en": "⬅️ Back"},
    "btn.forward": {"ru": "Вперёд ➡️", "en": "Next ➡️"},
    "btn.pick": {"ru": "{name}", "en": "{name}"},
    "btn.resume": {"ru": "▶️ Продолжить: {name} ({progress}%)", "en": "▶️ Resume: {name} ({progress}%)"},
    "btn.resume_incomplete_all": {
        "ru": "▶️ Продолжить все недокачанные",
        "en": "▶️ Resume All Incomplete",
    },
    "btn.refresh_list": {"ru": "🔄 Обновить список", "en": "🔄 Refresh List"},
    "btn.maintenance_cleanup_missing": {"ru": "🧹 Очистить missing", "en": "🧹 Cleanup missing"},
    "btn.maintenance_cleanup_stale": {"ru": "🧹 Очистить stale pending", "en": "🧹 Cleanup stale pending"},
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
