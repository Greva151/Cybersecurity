FROM python:3.12
RUN apt-get update
RUN pip install flask gunicorn
COPY ./chall /app

WORKDIR /app

RUN chmod +x ./gunicorn.sh
EXPOSE 5000
ENTRYPOINT ["./gunicorn.sh"]
#ENTRYPOINT ["python", "-m", "flask", "run", "--host=0.0.0.0"]