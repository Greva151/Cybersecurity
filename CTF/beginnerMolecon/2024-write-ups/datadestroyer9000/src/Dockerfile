FROM cybersecnatlab/socaz:python-3.11-alpine

WORKDIR /app
COPY . . 
CMD ["socaz", "-t", "120", "--bind", "5555", "--cmd", "/usr/local/bin/python3 main.py"]