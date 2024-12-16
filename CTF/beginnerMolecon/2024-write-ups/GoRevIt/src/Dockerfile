FROM cybersecnatlab/socaz:python-3.12-bookworm

RUN mkdir /chall

WORKDIR /chall

COPY * ./
COPY requirements.txt ./
RUN pip install -r requirements.txt
CMD ["socaz", "-t", "120", "--bind", "3240", "--cmd", "/usr/local/bin/python3 server.py"]
