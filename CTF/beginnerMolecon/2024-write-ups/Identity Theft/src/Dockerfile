FROM python:3.11-slim

RUN apt-get update && apt-get install -y postgresql
RUN pip install --no-cache-dir Flask pycryptodome gunicorn psycopg2-binary

WORKDIR /app

COPY ./challenge .

#RUN apt-get update && apt-get install -y dos2unix && rm -rf /var/lib/apt/lists/*
#RUN dos2unix ./gunicorn.sh
RUN chmod +x ./gunicorn.sh

EXPOSE 5000

ENTRYPOINT ["./gunicorn.sh"]
#CMD ["python", "app.py"]
