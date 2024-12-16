FROM cybersecnatlab/socaz:debian-bookworm

WORKDIR /chall

COPY --chmod=444 ./flag.txt .
COPY --chmod=555 ./main .

CMD ["socaz", "-t", "30", "-d", "--bind", "7070", "--cmd", "/chall/main"]
