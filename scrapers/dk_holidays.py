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
    url = "http://www.kalender-365.dk/helligdage/%s.html" % (year)

    response = requests.post(url)

    html = response.text

    soup = Soup(html)

    rows = soup.find("table", attrs={"class" : "table1"}).findAll("tr")
    del rows[0]

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

    days = []

    # Loop over the rows
    for row in rows:
        elements = row.findAll("td")

        # Locate the day in integer and month in string
        dayProg = re.compile(r"(?P<day>[0-9]*)\. (?P<month>[a-zA-Z]*) (?P<year>[0-9]*)?")
        groups = dayProg.search(unicode(elements[0].find("span").text))

        days.append({
            "date" : datetime.fromtimestamp(mktime(time.strptime("%s %s %s" % (
            functions.zeroPadding(groups.group("day")), months[groups.group("month")], year), "%d %m %Y"))),
            "title" : unicode(elements[2].find("a").text).replace(" %s" % (year),""),
            "link" : elements[2].find("a")["href"],
            "year" : year,
            "country" : "da-DK",
            "source" : "http://www.kalender-365.dk/helligdage/",
            "_updated" : datetime.now(),
            "_created" : datetime.now()
        })

    return {
        "status" : "ok",
        "days" : days
    }