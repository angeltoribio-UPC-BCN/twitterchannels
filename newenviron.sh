#!/bin/sh

virtualenv -p python3 ../twitterenv
source ../twitterenv/bin/activate
pip install django
pip install channels
pip install tweepy
pip install python-decouple