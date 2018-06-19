# mlrepricer

It's just being at the very start, we put things together.
At the end of June 2018 we want have a beta version.
Maybe this ressource is helpful. https://github.com/LantaoYu/MARL-Papers

# Right now best if you contact me. This guide outdates to fast :)

We provide you some modules you can use in your existing infrastructure.
It should be very easy to do so.
To support this we also have schema validations.

This is not a repricer. It should be used for statistical and ml analysis of your data.
It would be nice if we share statistic analysis and discuss them and validate them.
The data on it's own is not valueable. Still i think we shouldn't share it.
# But let's share models and the analysis itself
I already started to look at the linear regression for nonprime and prime listings.

# I think every amazon merchant should do some statistical analysis.
If you know some python, we should help them.

# Where are we going?
There won't be a service ever. You can see that by how flexible we build it, for datastorage, modularity.
We rather want to take some of the heavy lifting when you handle price data.
That's not only mws related. I like to start implementing some eBay prices too.
Also we should be able to validate flexible metadata from your ERP.
Really our strength is to offer building blocks for things everyone would spend hours to solve problems.
Where hundreds of people already solved this.
Instead you maybe want make this framework better:)

![](https://innotrade24.com/index.php/s/f8y4opak4BKes3J/preview)

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
We are supporting the mws python api sdk: https://github.com/python-amazon-mws/python-amazon-mws
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
For more uptodate guides please check out the notebooks.

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

listener.main()  # will pull and delete messages from sqs forever

helper.load_dataframe()  # returns the cleaned dataframe
```

## Objectives:
- get data
- dump all data in historic archive [  ]
- simple method match cheapest price [ ]
- use https://github.com/python-amazon-mws/python-amazon-mws to set new prices [ ]
- use different approaches for modelling [ ]

- nice visualizations with altair to get some insights [ ]
