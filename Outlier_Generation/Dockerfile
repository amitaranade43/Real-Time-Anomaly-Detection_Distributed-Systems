FROM python:3.9-slim-buster

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "generate_outliers.py"]
