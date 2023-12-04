import boto3
import os
import json

from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


app = Flask(__name__)

LOCALSTACK_HOST = os.getenv("LOCALSTACK_HOST", "localstack")
SQS_QUEUE_NAME = os.getenv("SQS_QUEUE_NAME", "test-queue")

Base = declarative_base()
engine = create_engine("sqlite:///messages.db")
Session = sessionmaker(bind=engine)
session = Session()


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, Sequence("message_id_seq"), primary_key=True)
    content = Column(String)

Base.metadata.create_all(engine)


@app.route("/")
def index():
    messages = session.query(Message).all()
    return render_template("index.html", messages=messages)


@app.route("/submit", methods=["POST"])
def submit():
    sqs = boto3.client(
        "sqs",
        endpoint_url=f"http://{LOCALSTACK_HOST}:4566",
        region_name="eu-west-2",
    )
    queue_url = sqs.get_queue_url(QueueName=SQS_QUEUE_NAME)["QueueUrl"]
    message_content = request.form.get("message_content")
    sqs.send_message(
        QueueUrl=queue_url, MessageBody=json.dumps({"content": message_content})
    )

    return redirect(url_for("index"))


@app.route("/result", methods=["POST"])
def receive_result():
    result = request.json.get("result")
    new_message = Message(content=result)
    session.add(new_message)
    session.commit()

    return "OK", 200


@app.route("/messages")
def messages():
    messages = session.query(Message).all()
    return render_template("messages.html", messages=messages)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
