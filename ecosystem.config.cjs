const port = 7001;

module.exports = {
  apps: [{
    name: `statira:${port}`,
    script: './statira/main.py',
    interpreter: 'venv/bin/python',
    env: {
      STA: 'production',
      PORT: port,
      PYTHONPATH: '.',
      UVICORN_RELOAD: 'false'
    },
    watch: false,
    instances: 1,
    exec_mode: 'fork',
    max_memory_restart: '1G',
    exp_backoff_restart_delay: 100,
    error_file: 'logs/error.log',
    out_file: 'logs/output.log',
    time: true,
    merge_logs: true,
    log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
    autorestart: true,
    max_restarts: 10,
    min_uptime: '1m'
  }]
} 
