FROM python:slim-bullseye

WORKDIR /app

COPY app /app

RUN pip install flask

CMD [ "python", "/app/__init__.py"]
