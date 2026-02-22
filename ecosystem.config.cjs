module.exports = {
  apps: [
    {
      name: "signal-bot-1",
      cwd: "./signal-bot-1",
      script: "main.py",
      interpreter: "python3",
      autorestart: true,
      max_restarts: 20,
      restart_delay: 3000,
      env: {
        PYTHONUNBUFFERED: "1",
      },
    },
    {
      name: "signal-bot-2",
      cwd: "./signal-bot-2",
      script: "main.py",
      interpreter: "python3",
      autorestart: true,
      max_restarts: 20,
      restart_delay: 3000,
      env: {
        PYTHONUNBUFFERED: "1",
      },
    },
    {
      name: "landing-signal",
      cwd: "./Landing-signal",
      script: "npm",
      args: "run preview -- --host 0.0.0.0 --port 4173",
      autorestart: true,
      max_restarts: 20,
      restart_delay: 3000,
      env: {
        NODE_ENV: "production",
      },
    },
  ],
};
