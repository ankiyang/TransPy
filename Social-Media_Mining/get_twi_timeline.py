#!/usr/bin/python3.5
# -*- coding: utf-8 -*-

from tweepy import Cursor
from twitter_client import get_twitter_client

client = get_twitter_client()
for status in Cursor(client.home_timeline).items(10):
    print(status.text)