FROM python:3.13.3-slim

WORKDIR /dcb

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["sh", "-c", "cd /dcb && exec python main.py"]