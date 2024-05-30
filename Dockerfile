FROM python:3.11

WORKDIR /usr/src/app

COPY req.txt ./

COPY . .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r req.txt && \
    pip install celery

RUN python manage.py collectstatic --noinput
RUN python manage.py makemigrations

CMD celery -A your_app_name worker --loglevel=info
