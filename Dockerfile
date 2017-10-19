FROM python:2

WORKDIR /usr/src/app
COPY sample_daemon.py ./

CMD [ "python", "-u", "./sample_daemon.py" ]