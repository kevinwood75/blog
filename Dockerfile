FROM tiangolo/uwsgi-nginx-flask:python3.6
ENV LISTEN_PORT 4000
COPY ./app /test/app
WORKDIR /test
RUN pip install -r /app/requirements.txt