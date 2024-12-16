FROM cybersecnatlab/socaz:python-3.11-alpine

WORKDIR /app
COPY . .
RUN pip install pycryptodome
CMD ["socaz", "-t", "120", "--bind", "3333", "--cmd", "/usr/local/bin/python3 main.py"]