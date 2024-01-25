#!/bin/bash
conda create -n content_creator python=3.10
conda activate content_creator
pip install -r requirements.txt
scrapy runspider trending_spider.py # this will get trending repositories
scrapy runspider info_spider.py # then, for each trending repository, it will extract info.
python main.py # generate all summaries and output files.