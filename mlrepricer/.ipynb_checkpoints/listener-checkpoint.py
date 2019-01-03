# -*- coding: utf-8 -*-

"""
Get messages save them locally and delete them from the queue.

It's very fast we get thousands messages per minute.
If the queue is empty we sleep for 20 seconds.
"""
import boto3
import xmltodict
import threading
import time
import datetime
import redis


from . import setup, helper


datafolder = f"{setup.configs['datafolder']}sub/"
region_name = setup.configs['region_name']
queuename = setup.configs['queuename']

sqsres = boto3.resource('sqs', region_name=region_name)
sqs = boto3.client('sqs', region_name=region_name)
queue = sqsres.get_queue_by_name(QueueName=queuename)


class Listener(threading.Thread):
    """Demon Thread read data from aws queue and dump in Database."""

    def run(self):
        """Thread should run only once."""
        print(f'Starting {self.name}')
        redis_main()


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
    d = [d[i:i + 10] for i in range(0, len(d), 10)]  # 10 is max batchsize
    for batch in d:
        entries = []
        for idx, receipt_handle in enumerate(batch):
            entries.append({'Id': str(idx), 'ReceiptHandle': receipt_handle})
        sqs.delete_message_batch(QueueUrl=queue.url, Entries=entries)


def quickparse_message(message):
    """We have to preparse it to get the timestamp and asin."""
    message = message[0]['Body']
    mparsed = xmltodict.parse(message)['Notification'][
        'NotificationPayload']['AnyOfferChangedNotification']
    asin = mparsed['OfferChangeTrigger']['ASIN']
    score = datetime.datetime.strptime(
        mparsed['OfferChangeTrigger']['TimeOfOfferChange'],
        "%Y-%m-%dT%H:%M:%S.%fZ").timestamp()
    return asin, score


def redis_main():
    """Recieves every 20 seconds a new queue and outputs into a redis."""
    r = redis.StrictRedis(**helper.rediscred, decode_responses=True)
    while True:
        queue = sqsres.get_queue_by_name(QueueName=queuename)
        numbermessages = int(queue.attributes['ApproximateNumberOfMessages'])
        print(numbermessages)
        for _ in range(numbermessages):
            message = receive_message().get('Messages', None)
            if message is None:
                break
            asin, score = quickparse_message(message)
            r.zadd(asin, float(score), str(message))
            r.sadd('updated_asins', asin)
            # delete_message(message)
        time.sleep(20)
