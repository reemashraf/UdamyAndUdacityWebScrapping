#!/bin/sh

scrapy crawl udemy
echo "udemy data is placed in mongodb in coursesdb database udemy document successfully"
scrapy crawl udacity
echo "udacity data is placed in mongodb in coursesdb database udacity document successfully"

python MongoConnectionScrapy.py
echo 'done'
