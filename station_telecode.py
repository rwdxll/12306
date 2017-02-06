#!/usr/bin/env python
# -*- coding:utf-8 -*

import os
import re
import sys
import time
import json
import requests
from pprint import pprint

station_url = "https://kyfw.12306.cn/otn/resources/js/framework/station_name.js"

headers = {
	"Connection":"keep-alive",
	"Content-Type":"text/html",
	"Cache-Control":"max-age=0",
	"User-Agent":"Mozilla/5.0 (Windows NT 10.0;WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
	"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
	"Accept-Encoding":"gzip,deflate,sdch,br",
	"Accept-Language":"zh-CN,zh;q=0.8"
	}

def get_station_telecode(url):
	stations_code = {}
	try:
		resp = requests.get(url,headers=headers,verify=False)
		try:
			patter = re.compile('([A-Z]+)\|([a-z]+)')
			items = dict(re.findall(patter,resp.content))
			stations_code = dict(zip(items.values(),items.keys()))
		except Exception as e:
			print(e)
		else:
			print(" \n-> Now,Number of the Railway Station  : {stationNum} ".format(stationNum=len(stations_code)))
			with open("stations_code.json",'w') as fs:
				json.dump(stations_code,fs)
	except requests.URLRequired:
		print(" -> A valid URL is required to make a reques.\n")
	except requests.ConnectionError:
		print(" -> Network connection error.\n")
		sys.exit()
	except requests.HTTPError:
		print(" -> An HTTP error occurred.\n")
	else:
		with open("station_name.js",'w') as f:
			f.writelines(resp.content)
	#pprint(stations_code,indent=4)
	return stations_code

station_telecode = get_station_telecode(station_url)
