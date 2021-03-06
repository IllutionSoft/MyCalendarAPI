from scrapers import dk_holidays
from scrapers import us_holidays
from pymongo import *
from datetime import *
from database import *

yearsToScrape = 10
currentDate = datetime.now()
currentYear = int(currentDate.strftime("%Y"))

holidays = []

for year in range(currentYear, currentYear+yearsToScrape):
     holidays = holidays + dk_holidays.holidays(year)["days"]
     holidays = holidays + us_holidays.holidays(year)["days"]

for holiday in holidays:
    db.holidays.update(
        {
            "link" : holiday["link"],
            "country" : holiday["country"],
            "year" : holiday["year"]
        },
        holiday,
        upsert=True
    )
