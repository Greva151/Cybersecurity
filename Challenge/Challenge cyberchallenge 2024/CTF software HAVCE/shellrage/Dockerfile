FROM ubuntu:22.04 as builder

RUN apt-get update && apt-get install -y \
    build-essential \
    libseccomp-dev \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /build

COPY ./src/*.h /build
COPY ./src/*.c /build

# Enable Full RELRO
RUN gcc -Wl,-z,relro,-z,now -o shellrage *.h *.c -lseccomp

FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    libseccomp2 \
    socat \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /build/shellrage /app/shellrage

RUN useradd -ms /bin/bash unprivileged

RUN mkdir /app/data && chown -R unprivileged /app/data

USER unprivileged

ENTRYPOINT socat -t 30 -T 30 -d TCP-LISTEN:1234,reuseaddr,fork EXEC:'/app/shellrage',stderr

