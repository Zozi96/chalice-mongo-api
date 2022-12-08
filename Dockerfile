FROM python:3.9.15-alpine3.17

EXPOSE 8000

WORKDIR /usr/src/code

COPY code .

RUN pip install -r requirements.txt

CMD [ "chalice", "local", "--host", "0.0.0.0" ]
