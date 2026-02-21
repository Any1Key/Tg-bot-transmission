# Tg-bot-transmission

[Русская версия](README.md)

Telegram bot for managing Transmission via a convenient Telegram menu:
- add `magnet` links and `.torrent` files
- select a destination system folder
- view download history
- view and resume incomplete torrents
- basic Transmission statistics
- pause/resume all torrents
- interface language switch (RU/EN)

## 1. Requirements

- Docker + Docker Compose
- Telegram Bot Token (via `@BotFather`)
- Access to Transmission RPC

## 2. Project Structure

- `bot/` - Telegram bot code (`aiogram`)
- `migrations/` - Alembic migrations
- `.env.example` - environment variables example
- `config.yml.example` - destination folders example
- `docker-compose.yml` - bot container
- `Dockerfile` - bot image

## 3. Installation and Run

### Step 1. Clone

```bash
git clone https://github.com/Any1Key/Tg-bot-transmission.git
cd Tg-bot-transmission
```

### Step 2. Configure `.env`

```bash
cp .env.example .env
```

Fill in `.env`:

```env
TOKEN=your_telegram_bot_token_here
TRANSMISSION_URL=http://your-nas-ip:9091/transmission/rpc
TRANSMISSION_USER=change_me_user
TRANSMISSION_PASS=change_me_password
ADMIN_USER_IDS=123456789
DATABASE_URL=sqlite+aiosqlite:///./data/bot.db
CONFIG_PATH=/app/config.yml
POLL_INTERVAL_SECONDS=45
THROTTLE_SECONDS=1.0
LOG_LEVEL=INFO
```

### Step 3. Configure Destination Folders

```bash
cp config.yml.example config.yml
```

Example `config.yml`:

```yaml
download_dirs:
  Movies: "/volume1/Download/complete/Films"
  TV Series: "/volume1/Download/complete/Serials"
  Music: "/volume1/Download/complete/Music"
  Other: "/volume1/Download/complete/Other"
```

Important: paths in `config.yml` must match the filesystem of the Transmission instance defined in `TRANSMISSION_URL` (usually an external NAS Transmission):
- `/volume1/Download/complete/...`

If paths do not match, completed torrents will fail to move from `incomplete` to the selected folder.

### Step 4. Start Containers

```bash
docker compose up -d --build bot
```

Recommended host folder structure:

- `/volume1/Download/incomplete` - temporary download location
- `/volume1/Download/complete/...` - final destination folders

In this setup Transmission downloads to `incomplete` and moves completed torrents to the selected `download_dir`.

### Step 5. Check

```bash
docker compose ps
docker compose logs --tail=100 bot
```

## 4. How to Use the Bot

### Add a Torrent

1. Send `magnet:?....` in chat
2. Bot shows the list of configured folders
3. Pick a folder with `📁 Select: ...`

Or send a `.torrent` file - the flow is the same.

### Main Menu

- `📊 Network Stats`
  - total downloaded/uploaded
  - current DL/UL speed
  - active torrents count

- `🗂️ System Folders`
  - shows folders from `config.yml`

- `📜 Download History`
  - list of torrents you added with current status
  - pagination (8 items per page)

- `⬇️ Incomplete Torrents`
  - list of not yet finished torrents
  - `▶️ Resume: ...` for a specific torrent
  - `▶️ Resume all incomplete`
  - `🔄 Refresh list`

- `⏸️ Pause all torrents`
  - stops all torrents in Transmission

- `▶️ Resume all torrents`
  - starts all torrents in Transmission

- `🏠 Open main menu`
  - shows main menu again

- `🌐 Language`
  - switch interface language (Русский / English)

### Commands

- `/start` - open main menu
- `/menu` - open main menu
- `/history` - history
- `/stats` - stats
- `/folders` - system folders
- `/incomplete` - incomplete torrents
- `/language` - choose interface language
- `/cancel` - reset current FSM action

## 5. How "Incomplete" Is Detected

A torrent is considered incomplete if any of these is true:
- `percentDone < 1.0`, or
- `leftUntilDone > 0`, or
- `isFinished == false`

If any completion condition is true (`percentDone >= 1`, `leftUntilDone <= 0`, or `isFinished == true`), torrent is not shown as incomplete.

## 6. Database and Migrations

- Default DB: SQLite (`/app/data/bot.db`)
- Migrations are applied automatically at bot startup:
  - startup command: `alembic upgrade head && python -m bot.main`

Apply migrations manually:

```bash
docker compose run --rm bot alembic upgrade head
```

## 7. Security

- Do not commit real `.env`
- Use a dedicated Transmission user with a strong password
- Set correct `ADMIN_USER_IDS`, otherwise access is denied for everyone

## 8. Troubleshooting

- Bot does not respond:
  - check `TOKEN` and `ADMIN_USER_IDS`
  - check logs: `docker compose logs --tail=200 bot`

- Torrent is not added:
  - check `TRANSMISSION_URL` connectivity
  - check `TRANSMISSION_USER` / `TRANSMISSION_PASS`

- Folders are not shown:
  - check `config.yml` and `download_dirs`

- Empty history:
  - history includes only torrents added through this bot

## 9. Project Update

```bash
git pull
docker compose up -d --build bot
```

## 10. Project Ownership

Copyright (c) 2026 Any1Key

## 11. Support the Author

If this project is useful, you can support the author:

- Card number: `2200 2480 0026 2096`
- Recipient: `Руслан`

Thank you for your support.

Donations are voluntary and do not create obligations.
