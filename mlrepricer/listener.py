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
import threading
import pandas as pd
import time

from . import setup, schemas, parser
from .example_destination import SQLite  # AzureSQL or your own


yaml = YAML(typ='unsafe')
yaml.default_flow_style = False

# Just replace SQLite with your database class
tableobject = schemas.pricemonitor(SQLite)()


datafolder = f"{setup.configs['datafolder']}sub/"
region_name = setup.configs['region_name']
queuename = setup.configs['queuename']

sqsres = boto3.resource('sqs', region_name=region_name)
sqs = boto3.client('sqs', region_name=region_name)
queue = sqsres.get_queue_by_name(QueueName=queuename)


class Listener (threading.Thread):
    """Demon Thread read data from aws queue and dump in SQLite."""

    def run(self):
        """This thread should only run once."""
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


def dump_message_toyaml(message):
    """Dump the message to a yaml file its fine for up to a few thousand."""
    messageid = message['MessageId']
    r = xmltodict.parse(message['Body'])
    with open(f'{datafolder}{messageid}.yaml', 'w') as f:
        yaml.dump(r, f)


def parse(message):
    """Parse the message and return a pandas dataframe."""
    r = xmltodict.parse(message['Body'])
    # here we call the parser.py file •=•
    return pd.DataFrame(parser.main(r))


def delete_message(d):
    """Delete the messages we have processed."""
    d = [d[i:i + 10] for i in range(0, len(d), 10)]  # 10 is max batchsize
    for batch in d:
        entries = []
        for idx, receipt_handle in enumerate(batch):
            entries.append({'Id': str(idx), 'ReceiptHandle': receipt_handle})
        sqs.delete_message_batch(QueueUrl=queue.url, Entries=entries)


def main():
    """Recieves every 20 seconds a new queue and outputs into a database."""
    tableobject.createtable  # inherited from destination

    while True:
        messagedf = pd.DataFrame()
        deletelist = []

        # get new queue, for new messages
        queue = sqsres.get_queue_by_name(QueueName=queuename)
        numbermessages = int(queue.attributes['ApproximateNumberOfMessages'])
        print(numbermessages)
        for _ in range(numbermessages):
            message = receive_message().get('Messages', None)
            if message is not None:
                message = message[0]
                messagedf = messagedf.append(parse(message))
                deletelist.append(message['ReceiptHandle'])

        messagedf.to_sql(tableobject.table, tableobject.conn,
                         dtype=tableobject.dtypes,
                         if_exists='append', index=False)
        delete_message(deletelist)
        time.sleep(20)
