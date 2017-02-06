#!/usr/bin/env python
# -*- coding:utf-8 -*

import os
import re
import sys
import time
import json
import ssl
import requests
from pprint import pprint

#
#加载车站编码文件
with open("stations_code.json",'r') as f:
	stations_code = json.load(f)

start_train_date = raw_input("-> Input Departure Date: ")
start_stations_name = stations_code[raw_input("-> Input Start Train Stations Name: ")]
end_stations_name = stations_code[raw_input("-> Input End Train Stations Name: ")]

print start_train_date,start_stations_name,end_stations_name

headers = {
	"Connection":"keep-alive",
	"Content-Type":"text/html",
	"Cache-Control":"max-age=0",
	"User-Agent":"Mozilla/5.0 (Windows NT 10.0;WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
	"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
	"Accept-Encoding":"gzip,deflate,sdch,br",
	"Accept-Language":"zh-CN,zh;q=0.8"
	}

def query_ticket(train_date,from_station,to_station):
	rp = ""

	try:
		requests.packages.urllib3.disable_warnings()
		requests.get("https://kyfw.12306.cn/otn/",verify=False)
	except requests.URLRequired:
		print(" -> A valid URL is required to make a reques.\n")
	except requests.ConnectionError:
		print(" -> Network connection error.\n")
		sys.exit()
	except requests.HTTPError:
		print(" -> An HTTP error occurred.\n")
		
	try:
		while 1:
			requests.packages.urllib3.disable_warnings()
			resp_query = requests.get("https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date={train_date}&leftTicketDTO.from_station={from_station}&leftTicketDTO.to_station={to_station}&purpose_codes=ADULT"
				.format(train_date=train_date,from_station=from_station,to_station=to_station),
				headers=headers,verify=False)
			rp = resp_query.content
			if resp_query.status_code == 200:
				break
	except Exception as e:
		print(e)

	return rp

results = dict(json.loads(query_ticket(start_train_date,start_stations_name,end_stations_name)))

print results