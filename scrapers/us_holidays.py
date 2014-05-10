#!/usr/bin/python
# -*- coding: utf8 -*-

import re
import time
from datetime import datetime
from time import mktime
import os

from bs4 import BeautifulSoup as Soup

import requests
import functions


def holidays(year):
    os.environ['TZ'] = 'Europe/Copenhagen'
    time.tzset()
    url = "http://www.calendar-365.com/holidays/%s.html" % (year)

    response = requests.post(url)

    html = response.text

    soup = Soup(html)

    rows = soup.find("table", attrs={"class" : "table1"}).findAll("tr")
    del rows[0]

    # Create an array of months mapping danish name->month number
    months = {}
    months["january"]    = "01"
    months["february"]   = "02"
    months["march"]     = "03"
    months["april"]     = "04"
    months["may"]       = "05"
    months["june"]      = "06"
    months["july"]      = "07"
    months["august"]    = "08"
    months["september"] = "09"
    months["october"]   = "10"
    months["november"]  = "11"
    months["december"]  = "12"

    days = []

    # Loop over the rows
    for row in rows:
        elements = row.findAll("td")

        # Locate the day in integer and month in string
        dayProg = re.compile(r"(?P<day>[0-9]*)\. (?P<month>[a-zA-Z]*)")
        groups = dayProg.search(unicode(elements[0].find("span").text))

        days.append({
            "date" : datetime.fromtimestamp(mktime(time.strptime("%s %s %s" % (
            functions.zeroPadding(groups.group("day")), months[groups.group("month")], year), "%d %m %Y"))),
            "title" : unicode(elements[2].find("a").text).replace(" %s" % (year),""),
            "link" : elements[2].find("a")["href"],
            "year" : year,
            "country" : "en-US",
            "source" : "http://www.calendar-365.com/holidays/",
            "_updated" : datetime.now(),
            "_created" : datetime.now()
        })

    return {
        "status" : "ok",
        "days" : days
    }