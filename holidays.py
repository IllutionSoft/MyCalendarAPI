from scrapers import dk_holidays
from pymongo import *
from datetime import *
from database import *

yearsToScrape = 10
currentDate = datetime.now()
currentYear = int(currentDate.strftime("%Y"))

holidays = []

for year in range(currentYear, currentYear+yearsToScrape):
     holidays = holidays + dk_holidays.holidays(year)["days"]

for holiday in holidays:
    db.holidays.insert(holiday)
