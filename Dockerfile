FROM python:3.12-bullseye

WORKDIR /app

RUN pip install -U pip
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["python3", "main.py"]
