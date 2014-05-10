#!/usr/bin/python
# -*- coding: utf8 -*-

import re
import time
from datetime import datetime, date
from time import mktime
import os

from bs4 import BeautifulSoup as Soup

import requests
import functions

def flag_days ():
	url = "http://hvorforflagerbussen.dk/flagdage/"

	response = requests.get(url)

	html = response.text

	soup = Soup(html)

   	rows = soup.findAll("tr")
   	rows.pop(0)

   	flag_days = []

   	# Create an array of months mapping danish name->month number
	months = {}
	months["januar"]    = "01"
	months["februar"]   = "02"
	months["marts"]     = "03"
	months["april"]     = "04"
	months["maj"]       = "05"
	months["juni"]      = "06"
	months["juli"]      = "07"
	months["august"]    = "08"
	months["september"] = "09"
	months["oktober"]   = "10"
	months["november"]  = "11"
	months["december"]  = "12"

	for row in rows:
		elements = row.findAll("td")

		# Locate the day in integer and month in string
		dayProg = re.compile(r"(?P<day>[0-9]*)\. (?P<month>[a-zA-Z]*)")
		groups = dayProg.search(elements[0].text)

		name = unicode(elements[1].text)
		flag_days.append({
			"name" : name,
			"date" : datetime.fromtimestamp(mktime(time.strptime("%s %s %s" % (
            functions.zeroPadding(groups.group("day")), months[groups.group("month")], date.today().year), "%d %m %Y"))),
            "region" : "copenhagen",
            "country" : "da_DK"
		})


	return {
		"status" : "ok",
		"days" : flag_days
	}