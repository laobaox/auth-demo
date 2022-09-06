FROM python:3.9-buster

# RUN apt install gcc libpq (no longer needed bc we use psycopg2-binary)

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

RUN mkdir -p /home/app
COPY auth_demo/ /home/app/auth_demo
COPY tests/ /home/app/tests/

WORKDIR /home/app
CMD python run_app.py