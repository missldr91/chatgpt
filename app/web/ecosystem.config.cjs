module.exports = {
  apps: [
    {
      name: 'pptx-frontend',
      script: 'npm',
      args: 'run dev',
      cwd: '/home/user/webapp/app/web',
      env: {
        NEXT_PUBLIC_API_URL: 'http://localhost:8000',
        PORT: 3000
      },
      watch: false,
      instances: 1,
      exec_mode: 'fork'
    }
  ]
}
