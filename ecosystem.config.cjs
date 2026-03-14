// Путь к проекту: по умолчанию /opt/signalbot. Для старого сервера: PROJECT_ROOT=/root/signalbot-1 pm2 start ecosystem.config.cjs
const PROJECT_ROOT = process.env.PROJECT_ROOT || "/opt/signalbot";

module.exports = {
  apps: [
    {
      name: "signal-bot-1",
      cwd: `${PROJECT_ROOT}/signal-bot-1`,
      script: `${PROJECT_ROOT}/signal-bot-1/main.py`,
      interpreter: `${PROJECT_ROOT}/signal-bot-1/venv/bin/python`,
      autorestart: true,
      max_restarts: 20,
      restart_delay: 3000,
      env: { PYTHONUNBUFFERED: "1" },
    },
    {
      name: "signal-bot-2",
      cwd: `${PROJECT_ROOT}/signal-bot-2`,
      script: `${PROJECT_ROOT}/signal-bot-2/main.py`,
      interpreter: `${PROJECT_ROOT}/signal-bot-2/venv/bin/python`,
      autorestart: true,
      max_restarts: 20,
      restart_delay: 3000,
      env: { PYTHONUNBUFFERED: "1" },
    },
    {
      name: "bonus-bot",
      cwd: `${PROJECT_ROOT}/BonusBotGPT`,
      script: `${PROJECT_ROOT}/BonusBotGPT/bot.py`,
      interpreter: `${PROJECT_ROOT}/BonusBotGPT/venv/bin/python`,
      autorestart: true,
      max_restarts: 20,
      restart_delay: 3000,
      env: { PYTHONUNBUFFERED: "1" },
    },
    {
      name: "landing-signal",
      cwd: `${PROJECT_ROOT}/Landing-signal`,
      script: "npx",
      args: "serve dist -l 4173 --no-clipboard",
      autorestart: true,
      max_restarts: 20,
      restart_delay: 3000,
      env: { NODE_ENV: "production" },
    },
  ],
};
