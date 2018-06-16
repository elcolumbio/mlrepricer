# -*- coding: utf-8 -*-

"""
Get messages save them locally and delete them from the queue.

It's very fast we get thousands messages per minute.
If the queue is empty we sleep for 20 seconds.
We store the messages in yamlfiles, it will create some markers like !!omap.
Besides that we use it for readability.
"""
import boto3
from ruamel.yaml import YAML
import xmltodict
import time
import threading
import pandas as pd
#import datetime

from . import setup, schemas, example_destination, parser
from .example_destination import SQLite, AzureSQL
from sqlalchemy import Table, Column, Integer, MetaData


yaml = YAML(typ='unsafe')
yaml.default_flow_style = False


tableobject = schemas.pricemonitor(SQLite)()
datafolder = f"{setup.configs['datafolder']}sub/"
region_name = setup.configs['region_name']
queuename = setup.configs['queuename']

sqsres = boto3.resource('sqs', region_name=region_name)
sqs = boto3.client('sqs', region_name=region_name)
queue = sqsres.get_queue_by_name(QueueName=queuename)


class Listener (threading.Thread):
    def run(self):
        print(f'Starting {self.name}')
        main()
        print(f'Exiting {self.name}')


def receive_message():
    """Request against aws sqs, one message at a time."""
    return sqs.receive_message(
        QueueUrl=queue.url,
        AttributeNames=['SentTimestamp'],
        MaxNumberOfMessages=1,
        MessageAttributeNames=['All'],
        VisibilityTimeout=0,
        WaitTimeSeconds=0)


def dump_message_toyaml(message):
    """Dumping the message to a yaml file its fine for up to a few thousand."""
    messageid = message['MessageId']
    r = xmltodict.parse(message['Body'])
    with open(f'{datafolder}{messageid}.yaml', 'w') as f:
        yaml.dump(r, f)


def dump_message_tosqlite(message):
    """Dumping the message to a to a SQLite database."""

    messageid = message['MessageId']
    r = xmltodict.parse(message['Body'])
    parsed = pd.DataFrame(parser.main(r))
    parsed.to_sql(tableobject.table, tableobject.conn,
                  if_exists='append', index=False)


def delete_message(message):
    """Delete the one actual message we were processing."""
    receipt_handle = message['ReceiptHandle']
    sqs.delete_message(
        QueueUrl=queue.url,
        ReceiptHandle=receipt_handle)


def main():
    tableobject.createtable  # inherited from destination

    while True:
        # get new queue, for new messages
        queue = sqsres.get_queue_by_name(QueueName=queuename)
        numbermessages = int(queue.attributes['ApproximateNumberOfMessages'])
        print(numbermessages)
        for _ in range(numbermessages):
            message = receive_message().get('Messages', None)
            if message is None:
                break
            message = message[0]
            # replace it with your processing method
            dump_message_tosqlite(message)
            # delete_message(message)
        time.sleep(20)
