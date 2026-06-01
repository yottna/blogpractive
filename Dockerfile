FROM python:3.10.12 // python --version으로 프로젝트 파이썬 버전 확인 후 수정 요

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput