FROM python:3.8.10

ENV PYTHONUNBUFFERED 2

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip && pip install -r requirements.txt


COPY . /app/

ENV FLASK_APP=app/run.py

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]