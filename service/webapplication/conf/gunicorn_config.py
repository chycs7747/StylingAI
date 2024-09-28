command = '/app/django_env/bin/gunicorn'
pythonpath = '/app/myproject'
bind = '0.0.0.0:8000'
workers = 3
timeout = 240  # 요청 처리 최대 시간 240초
graceful_timeout = 240  # 우아한 종료 대기 시간 240초
