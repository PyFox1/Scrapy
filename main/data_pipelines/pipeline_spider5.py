
import re
import datetime

from cheetah_server.models.ScrapedRun import ScrapedRun
from cheetah_server.server import create_app, db

def modify_item(item):

    # modify item
    ##############

    #date
    if '-' in item['date']:
        splitted_dates = item['date'].split()
        date2 = datetime.datetime.strptime(splitted_dates[2], '%d.%m.%y')
        day_date1 = int(splitted_dates[0].replace('.', ''))
        date1 = datetime.datetime(date2.year, date2.month, day_date1)
        item['date'] = [date1, date2]
    else:
        item['date'] = [datetime.datetime.strptime(item['date'],  '%d.%m.%y')]

    #distance
    distance = []
    for element in item['event']:
        if element == 'Marathon':
            distance.append(42.195)
        elif element == 'Halbmarathon':
            distance.append(21.0975)
        elif element == '10 Km':
            distance.append(10)
    item['distance'] = distance

    #zip city, country
    location = item['location']
    if str(location).strip():
        #zip
        zip = re.compile(r'[0-9]+').findall(str(location))
        item['zip'] = int(zip[0])

        #city
        location = str(location).replace(")", "")\
                                .replace("(", "")\
                                .replace(",", "")\
                                .replace("'", "")
        item['city'] = re.compile(r'(([a-zäöüß]+\s?)+)$', re.IGNORECASE).search(location).group()

        #country
        country = re.compile(r'^((CH)|(A))(\s)', re.IGNORECASE | re.VERBOSE).search(str(location)).group(1)
        for element in item['address_list']:
            if element.strip() in ["Deutschland", "Österreich", "Schweiz"]:
                item['country'] = element
            elif country == "A":
                item['country'] = "Österreich"
            elif country == "CH":
                item['country'] = "Schweiz"



    # only workaround, relational models neccessary
    item['event'] = ';'.join(item['event'])
    item['name'] = ';'.join(item['name'])
    item['distance'] = ';'.join(item['distance'])

    run_scraped = ScrapedRun(**item)
    app = create_app()
    app.app_context().push()
    db.session.add(run_scraped)
    db.session.commit()

    return item

