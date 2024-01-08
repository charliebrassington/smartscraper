FROM tiangolo/uwsgi-nginx:python3.11-2023-03-20

ENV LISTEN_PORT=5000
ENV UWSGI_INI uwsgi.ini

WORKDIR /app
COPY . /app/
COPY requirements.txt /app/

RUN pip install --no-cache-dir -U pip
RUN pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 5000