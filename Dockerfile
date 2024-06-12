FROM python:3.10

LABEL PROJECT_TITLE 'Patient Assessment System'

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/
RUN apt-get update && \ 
    pip install --no-cache-dir -r requirements.txt

COPY . /app/


EXPOSE 8004


ENTRYPOINT [ "bash","entrypoint.sh" ]


CMD uvicorn lib.core.asgi:application --host 0.0.0.0 --port 8004 --workers 4 --log-level debug --reload

