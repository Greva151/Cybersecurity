FROM cybersecnatlab/socaz:debian-bullseye

WORKDIR /app
COPY qaas /app/qaas

CMD ["socaz", "--bind", "0.0.0.0:5000", "--timeout", "300", "--cmd", "/app/qaas"]
