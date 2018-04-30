FROM tiangolo/uwsgi-nginx-flask:python3.6
ENV LISTEN_PORT 4000

COPY ./app /app
WORKDIR /
RUN pip install -r requirements.txt