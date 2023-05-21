FROM tiangolo/uvicorn-gunicorn:python3.8

WORKDIR /app


LABEL maintainer="Sebastian Ramirez <tiangolo@gmail.com>"

COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY ./backend /backend

COPY ./ ./

CMD ["uvicorn", "main:app", "--reload"]
