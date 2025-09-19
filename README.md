🛡️ ModerationBot

    A modern, purple-themed Discord moderation bot with slash-commands, real-time PostgreSQL backend and custom-command engine.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![discord.py](https://img.shields.io/badge/discord.py-2.3+-5865F2?style=flat&logo=discord&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-4169E1?style=flat&logo=postgresql&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green.svg)

✨ Features

Command	Description

    /kick	Remove a member (with reason)
    /ban / /unban	Permanent ban / lift ban by ID
    /purge	Bulk-delete messages (1-100)
    /warn / /warns	Issue / list member warnings (stored in PG)
    /ping / /avatar	Utility with style
    /addcmd / /delcmd	Create server-specific shortcuts
    Purple embeds – every bot response is color-coordinated
    PostgreSQL backend – warnings & custom commands persist between restarts
    Slash only – modern, no-prefix UX

🚀 Quick Start (openSUSE / any systemd Linux)

    # 1. Clone & enter repo
    git clone https://github.com/YOU/ModerationBot.git && cd ModerationBot

    # 2. Install PostgreSQL + Python deps
    sudo zypper in postgresql-server python3.13-devel gcc
    sudo systemctl start postgresql && sudo systemctl enable postgresql

    # 3. Create bot DB & user
    sudo -u postgres createuser -P $USER
    sudo -u postgres createdb moderationbot -O $USER

    # 4. Python environment
    python3 -m venv venv && source venv/bin/activate
    pip install -r requirements.txt

    # 5. Configure
    cp .env.example .env
    # edit .env – paste BOT_TOKEN from Discord Dev Portal and PG_DSN
    nano .env

    # 6. Invite bot (permissions: Kick/Ban/ManageMessages/ModerateMembers)
    # URL is printed after first run – or generate manually:
    # https://discord.com/oauth2/authorize?client_id=YOUR_ID&scope=applications.commands+bot&permissions=274877910080

    # 7. Run
    python3 bot.py

Bot logs in and syncs slash commands globally – they appear instantly in every server.

⚙️ Environment Variables

Variable	Example	Purpose
BOT_TOKEN	OTk3N…	Discord token (keep secret)
PG_DSN	postgresql://m1nem:StrongPass@localhost:5432/moderationbot	PostgreSQL connection string

🐳 Docker (optional)

    FROM python:3.13-slim
    WORKDIR /app
    COPY requirements.txt .
    RUN pip install -r requirements.txt
    COPY . .
    CMD ["python3", "bot.py"]

Build & run:

    docker build -t moderation-bot .
    docker run -d --env-file .env moderation-bot

📜 Commands Reference

Slash Command	Permission	Description
/kick	Kick Members	Remove member with reason
/ban	Ban Members	Permanent ban
/unban	Ban Members	Lift ban by Discord ID
/purge	Manage Messages	Bulk-delete (1-100)
/warn	Moderate Members	Issue warning (stored in PG)
/warns	—	List member warnings
/ping	—	Bot latency
/avatar	—	Show user avatar
/addcmd	Manage Guild	Create server shortcut
/delcmd	Manage Guild	Delete shortcut
All responses use purple embeds for consistent look.

🛠️ Tech Stack

    Language: Python 3.13+
    Library: discord.py 2.3 (modern async)
    DB: PostgreSQL 17+ (asyncpg)
    Commands: Discord Slash Commands (no legacy prefix needed)
    Theming: #9b59b6 purple embeds

🤝 Contributing

    Fork the repo
    Create feature branch (git checkout -b feature/amazing)
    Commit & push (git commit -m "Add amazing feature")
    Open a Pull Request

📄 License
MIT © 2025 m1nem – feel free to use, modify and distribute.
⭐ Star the repo if you like the bot – it helps a lot!