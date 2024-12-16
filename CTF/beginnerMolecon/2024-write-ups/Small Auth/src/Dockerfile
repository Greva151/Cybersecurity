FROM cybersecnatlab/socaz:debian-bullseye

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    && rm -rf /var/lib/apt/lists/*

RUN pip install pycryptodome

COPY server.py .
COPY secret.py .

CMD ["socaz", "--bind", "1337", "--", "python3", "./server.py"]