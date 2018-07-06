FROM python:alpine3.7

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["gunicorn", "-w1", "-b :5000", "main:app"]
