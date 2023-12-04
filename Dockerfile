FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt .
COPY .flaskenv .

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["flask", "run"]
