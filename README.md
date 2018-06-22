# mlrepricer

Everyone is welcome to contribute.
There are lots of improvements needed.


One perspective is from a Multi Agent Problem.
Maybe it's over the top and the problem is simpler and quite static?

Some ressources about Multi Agent learning:
https://github.com/LantaoYu/MARL-Papers
https://www.youtube.com/watch?v=yE62Zwhmzi8
https://www.youtube.com/watch?v=bjjoHji8KUQ


We provide you some modules you can use in your existing infrastructure.
It should be very easy to do so.

Lately we switched to redis.
We still have schema validations for sql, need some work to integrate the missing parts.

This is not a repricer. It should be used for statistical and ml analysis of your data.
It would be nice if we share statistic analysis and discuss them and validate them.
The data on it's own is not valueable.

The linear regression for nonprime and prime listings, we can find.


# I think every amazon merchant should do some statistical analysis.
If you know some python, we should help you.

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
ruamel
redis
numpy
jupyterlab

and others for prediction

## How to get started?
For more uptodate guides please check out the notebooks.

Setup Boto3 credentials for aws sqs:
~/.aws/credentials:
```
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
```

We define all configs in a yaml file, if you fill out everything you are fine.
So copy mlrepricer/mlrepricer/configs.yaml to the default location ~/.config/mlrepricer/configs.yaml .
Or change the path_to_config in the setup package.

## Installation
You can clone it locally and cd into the top level folder.
and install it with: pip install .

## Usage
See the notebooks. Download this repo and unpack it, or render them in github.
