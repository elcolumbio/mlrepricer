# -*- coding: utf-8 -*-

"""
Get messages save them in your redis database and delete them from the queue.

It's very fast we can get thousands messages per minute.
If the queue is empty we sleep for 20 seconds.
"""
import boto3
import datetime
import redis
import threading
import time
import xmltodict

from . import setup, helper


datafolder = f"{setup.configs['datafolder']}sub/"
region_name = setup.configs['region_name']
queuename = setup.configs['queuename']

sqsres = boto3.resource('sqs', region_name=region_name)
sqs = boto3.client('sqs', region_name=region_name)
queue = sqsres.get_queue_by_name(QueueName=queuename)


class Listener(threading.Thread):
    """Demon thread read data from aws queue and dump in Database."""

    def run(self):
        """Thread should run only once."""
        print(f'Starting {self.name}')
        main()


def receive_message():
    """Request against aws sqs, one message at a time."""
    return sqs.receive_message(
        QueueUrl=queue.url,
        AttributeNames=['SentTimestamp'],
        MaxNumberOfMessages=1,
        MessageAttributeNames=['All'],
        VisibilityTimeout=600,  # so long we have one thread it's ok
        WaitTimeSeconds=0)


def delete_message(d):
    """Delete the messages we have processed."""
    if isinstance(d, str):
        sqs.delete_message(QueueUrl=queue.url, ReceiptHandle=d)
    else:  # deprecated bulk deleting
        d = [d[i:i + 10] for i in range(0, len(d), 10)]  # 10 is max batchsize
        for batch in d:
            entries = []
            for idx, receipt_handle in enumerate(batch):
                entries.append(
                    {'Id': str(idx), 'ReceiptHandle': receipt_handle})
            sqs.delete_message_batch(QueueUrl=queue.url, Entries=entries)


def quickparse_message(message):
    """We have to pre-parse it to get the timestamp and asin."""
    message_parsed = xmltodict.parse(message[0]['Body'])
    receipt_handle = message[0]['ReceiptHandle']
    payload = message_parsed['Notification']['NotificationPayload'][
        'AnyOfferChangedNotification']['OfferChangeTrigger']
    asin = payload['ASIN']
    score = datetime.datetime.strptime(
        payload['TimeOfOfferChange'], "%Y-%m-%dT%H:%M:%S.%fZ").timestamp()
    return asin, score, receipt_handle


def start_database():
    """We use redis as the default, feel free to use whatever you want."""
    # ToDO for windows WSL how to i start the redis server?
    return redis.StrictRedis(**helper.rediscred, decode_responses=True)


def store_into_database(db, asin, score, message):
    """Store the complete message from the aws queue, we parse it later."""
    db.zadd(asin, float(score), str(message))
    # better use pub/sub
    db.sadd('updated_asins', asin)  # memo that we have to take action
    return True


def main():
    """
    Sleeps 20 seconds after calls to the aws queue and dump into database.

    You should be able to use another database, if you only want to bulk write
    to your database we need to alter the design a bit.
    """
    db = start_database()  # database specific
    while True:
        queue = sqsres.get_queue_by_name(QueueName=queuename)
        numbermessages = int(queue.attributes['ApproximateNumberOfMessages'])
        print(numbermessages)
        for _ in range(numbermessages):
            message = receive_message().get('Messages', None)
            if message is None:
                break
            asin, score, receipt_handle = quickparse_message(message)
            # database specific, here we delete one message a time
            if store_into_database(db, asin, score, message):
                delete_message(receipt_handle)

        time.sleep(20)
