FROM python:3.11-bullseye

WORKDIR /app

RUN pip install -U pip
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get -y install libopus-dev

COPY . .
CMD ["python3", "main.py"]
