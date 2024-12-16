FROM cybersecnatlab/socaz:debian-bookworm

RUN mkdir /app
WORKDIR /app

COPY ./challenge /app/challenge
COPY ./flag.txt /app/flag.txt

CMD ["socaz", "-t", "120", "--bind", "1338", "--cmd", "/app/challenge"]