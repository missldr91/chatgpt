module.exports = {
  apps: [
    {
      name: 'pptx-frontend',
      script: 'npm',
      args: 'run dev',
      cwd: '/home/user/webapp/app/web',
      env: {
        NEXT_PUBLIC_API_URL: 'https://8000-ieq6xwbj6bsk4tk4gpuij-6532622b.e2b.dev',
        PORT: 3000
      },
      watch: false,
      instances: 1,
      exec_mode: 'fork'
    }
  ]
}
