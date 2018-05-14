# mlrepricer
A python pricing analysis project for Amazon Marketplace Sellers.
Plus we provide the basic box where you can run your ml algorithms.

### price volatility of buyboxwinners

![volatility](https://innotrade24.com/index.php/s/RR9WWwGgFJGXjTL/preview)

You can use methods for easy access and training models.
If we use the same features we can find a more accurate model, together.
A repricer model is quite complex.
It's like scissors and papers with price elasticity and estimates about sales.
For the start we can make it as simple as possible.
If this is going very well, we will build a live repricer which is constantly learning.

## Dependencies
boto3
ruamel
xmltodict
pandas

## Data structure
Define a datafolder.
- datafolder/
    - sub/    <- here we put all messages as single files, so we can rebuild our features.
    - alldata    <- this is the msgpack datafram we work with, it's cleaned and ready to use for training.
    
 it's a lot of data we might do this more clever. Right now it seems to work, it should not take too much space.
 7.011 items, totalling 46,5 MB

## Questions to ask
Should we start with continously evaluating the outcome?
If yes we have to build all the basic parts first.

So what type of problem we want to solve?

## How to get started?


Setup Boto3 credentials for aws sqs:
~/.aws/credentials:
```
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
```

We define all configs in a yaml file.
So copy mlrepricer/mlrepricer/configs.yaml to the default location ~/.config/mlrepricer/configs.yaml .
Or change the path_to_config in the setup package.

## Installation
You can clone it locally and cd into the top level folder.
and install it with: pip install .

## Usage
this shoud work right now:
```python
from mlrepricer import helper
from mlrepricer import listener, parser

listener()  # will pull and delete messages from sqs forever

helper.load_dataframe()  # returns the cleaned dataframe
```

## Objectives:
- get data
- dump all data in historic archive [  ]
- simple method match cheapest price [ ]
- use https://github.com/python-amazon-mws/python-amazon-mws to set new prices [ ]
- use different approaches for modelling [ ]

- nice visualizations with altair to get some insights [ ]
