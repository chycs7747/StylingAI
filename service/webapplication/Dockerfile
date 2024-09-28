# 베이스 이미지 선택
FROM python:alpine3.20

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 패키지 업데이트 및 필요한 패키지 설치
RUN apk update && apk add --no-cache \
    build-base \
    libpq-dev \
    postgresql-dev \
    gcc \
    musl-dev \
    linux-headers \
    python3-dev \
    py3-pip \
    bash

# 프로젝트 파일 및 Gunicorn 설정 파일 복사
COPY myproject /app/myproject
COPY conf /app/conf

# 가상 환경 설치 및 생성
RUN python3 -m venv django_env

# 가상 환경 활성화 및 패키지 설치
RUN /bin/sh -c "source django_env/bin/activate && \
    pip install --no-cache-dir django==4.2.13 gunicorn django-cors-headers djangorestframework markdown django-filter boto3 pillow==10.3.0 requests"

# 정적 파일 수집 (옵션)
RUN /bin/sh -c "source django_env/bin/activate && \
    python /app/myproject/manage.py collectstatic --noinput"

# 환경 변수 설정
ENV DJANGO_SETTINGS_MODULE=myproject.settings
ENV PYTHONUNBUFFERED 1

# Gunicorn 실행
CMD ["/bin/sh", "-c", "source django_env/bin/activate && gunicorn -c /app/conf/gunicorn_config.py myproject.wsgi"]
