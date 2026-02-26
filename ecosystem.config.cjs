// Перед первым запуском на сервере: cd /root/signalbot-1 && git pull origin main
// Убедись что есть: signal-bot-1/main.py, signal-bot-2/main.py, BonusBotGPT/bot.py, Landing-signal/dist/
module.exports = {
  apps: [
    {
      name: "signal-bot-1",
      cwd: "/root/signalbot-1/signal-bot-1",
      script: "/root/signalbot-1/signal-bot-1/main.py",
      interpreter: "/root/signalbot-1/signal-bot-1/venv/bin/python",
      autorestart: true,
      max_restarts: 20,
      restart_delay: 3000,
      env: { PYTHONUNBUFFERED: "1" },
    },
    {
      name: "signal-bot-2",
      cwd: "/root/signalbot-1/signal-bot-2",
      script: "/root/signalbot-1/signal-bot-2/main.py",
      interpreter: "/root/signalbot-1/signal-bot-2/venv/bin/python",
      autorestart: true,
      max_restarts: 20,
      restart_delay: 3000,
      env: { PYTHONUNBUFFERED: "1" },
    },
    {
      name: "bonus-bot",
      cwd: "/root/signalbot-1/BonusBotGPT",
      script: "/root/signalbot-1/BonusBotGPT/bot.py",
      interpreter: "/root/signalbot-1/BonusBotGPT/venv/bin/python",
      autorestart: true,
      max_restarts: 20,
      restart_delay: 3000,
      env: { PYTHONUNBUFFERED: "1" },
    },
    {
      name: "landing-signal",
      cwd: "/root/signalbot-1/Landing-signal",
      script: "npx",
      args: "serve dist -l 4173 --no-clipboard",
      autorestart: true,
      max_restarts: 20,
      restart_delay: 3000,
      env: { NODE_ENV: "production" },
    },
  ],
};
