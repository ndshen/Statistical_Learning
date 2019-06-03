#%%
from bs4 import BeautifulSoup
import requests
import csv
import os.path

FILE = 'cwb.csv'
URL = "https://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do?command=viewMain&station=467480&stname=%25E5%2598%2589%25E7%25BE%25A9&datepicker={year}-{month}-{day}#"
HEADER =  ['Month','Day','ObsTime', 'StnPres', 'SeaPres', 'Temperature', 'Td dew point', 'RH', 'WS', 'WD', 'WSGust', 'WDGust', 'Precp', 'PrecpHour', 'SunShine', 'GloblRad', 'Visb', 'UVI', 'Cloud Amount','Year']

def single_day_to_excel(year, month, day, csv_file=FILE):
    url = URL.format(year=str(year), month="{:02d}".format(month), day="{:02d}".format(day))
    res = requests.get(url)
    page = res.text
    soup = BeautifulSoup(page, "html.parser")

    table = soup.find('table', attrs={'id':'MyTable'})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')

    data = []
    for row in rows[3:]:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            cols.insert(0, str(month))
            cols.insert(1, str(day))
            cols.append(str(year))
            data.append(cols)

    with open(csv_file, "a", newline='') as f:
        writer = csv.writer(f)
        for row in data:
            writer.writerow(row)

#%%
BIG_MONTH = {1,3,5,7,8,10,12}

if os.path.isfile(FILE) is not True:
    with open(FILE, "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(HEADER)

for m in range(4,13):
    if m in BIG_MONTH:
        days = 31
    elif m == 2:
        days = 28
    else:
        days = 30
    for d in range(1, days+1):
        single_day_to_excel(2018, m, d)
        print("Year: {}, Month: {}, Day: {}".format(2018, m, d))


for m in range(1,5):
    if m in BIG_MONTH:
        days = 31
    elif m == 2:
        days = 28
    else:
        days = 30
    for d in range(1, days+1):
        single_day_to_excel(2019, m, d)
        print("Year: {}, Month: {}, Day: {}".format(2019, m, d))

    