FROM python:3.12-alpine3.19

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY run.py .

COPY ./app .

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
