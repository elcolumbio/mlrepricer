# mlrepricer
A python repricer project for Amazon Marketplace Sellers.

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

## Questions to ask
Should we start with continously evaluating the outcome?
If yes we have to build all the basic parts first.

So what type of problem we want to solve?

## How to get started?
Boto3 looks for credentials in:

~/.aws/credentials:
```
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
```

We define all configs in:
mlrepricer/mlrepricer/configs.yaml
So copy that file anywhere. Best not in the repository, since it is sensible data.
Define the path_to_config in the setup package.

## Objectives:
- get data
- dump all data in historic archive
- simple method match cheapest price
- use https://github.com/python-amazon-mws/python-amazon-mws to set new prices
- use different approaches for modelling
