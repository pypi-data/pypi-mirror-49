Estimator
=========

[![Pipeline Status](https://gitlab.com/chrisspen/estimator/badges/master/pipeline.svg)](https://gitlab.com/chrisspen/estimator/commits/master) 
[![PyPI Status](https://img.shields.io/pypi/v/estimator.svg)](https://pypi.python.org/pypi/estimator)

A Python script for automatically estimating work hours in Jira using supervised learning.

Installation
------------

Install the Python 3 package:

    pip install estimator

Usage
-----

Fill out the login credentials in your `config.yaml`.

Retrieve training data:

    estimator.py config.yaml retrieve

Generate all possible algorithm and setting combinations:

    estimator.py config.yaml generation-combinations

Test all combinations to find which algorithm works best:

    estimator.py config.yaml test-combinations

Fill in the `regressor` settings in your `config.yaml`, then train your final regressor:

    estimator.py config.yaml train

Find the algorithm's accuracy:

    estimator.py config.yaml test

Dryrun the application of the regressor to unestimated tickets:

    estimator.py config.yaml apply

Save these estimates with:

    estimator.py config.yaml apply --save

To combine the above retrieve, train and apply steps into a single command, just add `--retrain` to the apply command:

    estimator.py config.yaml apply --save --retrain

Development
-----------

Run tests locally with:

    tox

To run tests for a specific environment (e.g. Python 3.7):
    
    tox -e py37

To run a specific test:
    
    export TESTNAME=.test_learning; tox -e py37
