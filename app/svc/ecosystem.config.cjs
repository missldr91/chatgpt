module.exports = {
  apps: [
    {
      name: 'pptx-backend',
      script: 'venv/bin/uvicorn',
      args: 'app.main:app --host 0.0.0.0 --port 8000 --reload',
      cwd: '/home/user/webapp/app/svc',
      env: {
        PYTHONUNBUFFERED: '1',
        CORS_ORIGINS: 'http://localhost:3000'
      },
      watch: false,
      instances: 1,
      exec_mode: 'fork'
    }
  ]
}
